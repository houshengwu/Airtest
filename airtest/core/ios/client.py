#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import sys
# sys.path.append("..")
# from error import MoaError
from airtest.core.error import MoaError
import utils
from airtest.aircv import aircv
from airtest.core.device import Device
from constant import *
from hunter_cli import Hunter
import time
import wda
import airtest
from cStringIO import StringIO
import base64
from PIL import Image



# class XYTransformer(object):
#     """
#     transform xy by orientation
#     add by gzzhengshenshen, it is different with android
#     """
# 
#     @staticmethod
#     def up_2_ori((x, y), (w, h), orientation):
#         if orientation == 1:
#             x, y = y, w - x
#         elif orientation == 2:
#             x, y = w - y, h - x
#         elif orientation == 3:
#             x, y = h - y, x
#         return x, y
        

class IOS(Device):
    """ios client
        # befor this you have to run WebDriverAgent
        # xcodebuild -project path/to/WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination "id=$(idevice_id -l)" test
        # iproxy $port 8100 $udid
    """

    def __init__(self, udid):
        super(Device, self).__init__()
        self.udid = udid

        # auto detect local device or remote device. using default 8100 port for local device's wda
        if ':' in udid:
            device_url = 'http://{}'.format(udid)
        else:
            device_url = 'http://localhost:8100'

        # wda driver, use to tap home, start app
        # init wda session, updata when start app
        # use to click/swipe/close app/get wda size
        self.driver = wda.Client(device_url)
        wda_status = self.driver.status()
        session_id = wda_status['sessionId']
        self.session = wda.Session(device_url, session_id)

        # init display info
        # attention：there is 3 size,phy_size/pic_size/wda_size
        self.get_display_info()

    def shell(self):
        raise NotImplementedError

    def home(self):
        self.driver.home()

    def snapshot(self, filename=None):
        return self._snapshot(filename)
        
    def _snapshot(self, filename=None):
        """
        take snapshot
        filename: save screenshot to filename
        """
        filename = filename or "tmp.png"
        data = utils.screenshot(self.udid)
        file_data = StringIO(data)
        image = Image.open(file_data)
        method = getattr(Image, 'ROTATE_{}'.format(self.size["rotation"]))
        image = image.transpose(method)
        image.save(filename)
        with open(filename) as f:
            data = f.read()
        # 输出cv2对象
        screen = aircv.string_2_img(data)
        return screen

    def touch(self, pos, duration=None):
        self.session.tap(pos[0] / self.wda_sca, pos[1] / self.wda_sca)

    def swipe(self, fpos, tpos, duration=0.5, step=4):
        self.session.swipe(fpos[0] / self.wda_sca, fpos[1] / self.wda_sca,
                           tpos[0] / self.wda_sca, tpos[1] / self.wda_sca, step)

    def keyevent(self):
        raise NotImplementedError

    def text(self, text):
        """you need to click textfield first"""
        self.session.send_keys(text)

    def start_app(self, appid):
        """launch an app by appid"""
        self.session = self.driver.session(appid)

    def stop_app(self, appid):
        """stop an app by appid"""
        self.session.close()

    def clear_app(self, upload_file_path):
        utils.cleanup(upload_file_path, self.udid)

    def install_app(self, filepath, reinstall=True, appid=None):
        if reinstall:
            utils.uninstall_app(appid, self.udid)
        upload_file_path = utils.upload_file(filepath, udid=self.udid)
        utils.install_file(upload_file_path)
        self.clear_app(upload_file_path)

    def uninstall_app(self, appid):
        utils.uninstall_app(appid, self.udid)

    def get_display_info(self):
        self.size = {}
        self.size["orientation"] = self.getDisplayOrientation()
        self.size["rotation"] = self.size["orientation"] * 90
        self.size["height"], self.size["width"] = self.getPhysicalDisplayInfo()
        self.wda_sca = 1.0 * min(self.size["height"], self.size["width"]) / min(self.session.window_size())
        print self.size
        return self.size

    def getPhysicalDisplayInfo(self):
        """
        get size of screen, height must be bigger then width
        """
        screen = self._snapshot(filename="init_phy.png")
        h, w = screen.shape[:2]
        return h, w

    def getDisplayOrientation(self):
        """
        return orientation code
        """
        return utils.get_orientation(self.udid)

    # use to resize
    def getCurrentScreenResolution(self):
        w, h = self.size["width"], self.size["height"]
        return w, h

    def refreshOrientationInfo(self, ori=None):
        """
        update dev orientation
        if ori is assigned, set to it(useful when running a orientation monitor outside)
        """
        if ori is None:
            ori = self.getDisplayOrientation()
        self.size["orientation"] = ori
        self.size["rotation"] = ori * 90


if __name__ == "__main__":
    ios = IOS('10.251.93.160:8100')
    ios.start_app('com.netease.mhxyhtb')
    ios.stop_app('com.netease.mhxyhtb')
    # driver.home()
    #driver.touch((333, 272))
    #(421, 435) (476, 436)
    #driver.touch((200,100))
    # driver.swipe((150, 450) ,(150, 100))
    #driver.touch((0, 0),isWDA=True)
    #driver.text("123")