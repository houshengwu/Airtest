# -*- coding: utf-8 -*-
from airtest.utils.logger import get_logger
from airtest.utils.safesocket import SafeSocket
from airtest.utils.nbsp import NonBlockingStreamReader
from airtest.utils.snippet import reg_cleanup
import struct
LOGGING = get_logger('javacap')


class Javacap(object):

    """another screencap class, slower than minicap, but better compatibility
       bug to be fixed: get_frame will return cached old screen, not always current screen
    """

    APP_PKG = "com.netease.nie.yosemite"
    SCREENCAP_SERVICE = "com.netease.nie.yosemite.Capture"
    RECVTIMEOUT = None

    def __init__(self, adb):
        self.adb = adb
        self.frame_gen = None
        reg_cleanup(self.teardown_stream)

    def _setup_stream_server(self):
        localport, deviceport = self.adb.setup_forward("localabstract:javacap_{}".format)
        deviceport = deviceport[len("localabstract:"):]
        # setup agent proc
        apkpath = self.adb.path_app(self.APP_PKG)
        cmds = ["CLASSPATH=" + apkpath, 'exec', 'app_process', '/system/bin', self.SCREENCAP_SERVICE,
                "--scale", "100", "--socket", "%s" % deviceport, "-lazy", "2>&1"]
        proc = self.adb.start_shell(cmds)
        # check proc output
        nbsp = NonBlockingStreamReader(proc.stdout, print_output=True, name="javacap_sever")
        while True:
            line = nbsp.readline(timeout=5.0)
            if line is None:
                raise RuntimeError("javacap server setup timeout")
            if "Capture server listening on" in line:
                break
            if "Address already in use" in line:
                raise RuntimeError("javacap server setup error: %s" % line)
        return proc, nbsp, localport

    def get_frames(self):
        proc, nbsp, localport = self._setup_stream_server()
        s = SafeSocket()
        s.connect((self.adb.host, localport))
        t = s.recv(24)
        # javacap header
        LOGGING.debug(struct.unpack("<2B5I2B", t))

        stopping = False
        while not stopping:
            s.send(b"1")
            # recv frame header, count frame_size
            if self.RECVTIMEOUT is not None:
                header = s.recv_with_timeout(4, self.RECVTIMEOUT)
            else:
                header = s.recv(4)
            if header is None:
                LOGGING.error("javacap header is None")
                # recv timeout, if not frame updated, maybe screen locked
                stopping = yield None
            else:
                frame_size = struct.unpack("<I", header)[0]
                frame_data = s.recv(frame_size)
                stopping = yield frame_data

        LOGGING.debug("javacap stream ends")
        s.close()
        nbsp.kill()
        proc.kill()
        self.adb.remove_forward("tcp:%s" % localport)

    def get_frame_from_stream(self):
        if self.frame_gen is None:
            self.frame_gen = self.get_frames()
        return self.frame_gen.send(None)

    def teardown_stream(self):
        if not self.frame_gen:
            return
        try:
            self.frame_gen.send(1)
        except (TypeError, StopIteration):
            pass
        else:
            LOGGING.warn("%s tear down failed" % self.frame_gen)
        self.frame_gen = None
