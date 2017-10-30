# -*- coding: utf-8 -*-
import win32gui
import win32api
import win32ui
import win32con


SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79


def screenshot(filename, hwnd=None):
    if hwnd is None:
        """all screens"""
        hwnd = win32gui.GetDesktopWindow()
        # get complete virtual screen including all monitors
        w = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
        h = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
        x = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
        y = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)
    else:
        """window"""
        rect = win32gui.GetWindowRect(hwnd)
        w = abs(rect[2] - rect[0])
        h = abs(rect[3] - rect[1])
        x, y = 0, 0

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)