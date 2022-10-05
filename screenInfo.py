import win32api
import win32con


class screenInfo:
    def __init__(self):
        self.X = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.Y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    def get_w(self):
        return win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 获得屏幕分辨率X轴

    def get_h(self):
        return win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 获得屏幕分辨率Y轴
