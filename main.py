#########################################
#   create by hjx                       #
#   version alpha 0.1.5                 #
#   2022/5/14                           #
#                                       #
#########################################

import time
import autopy
import cv2
import numpy as np
import pyautogui

import screenInfo
import handProcess
from utils import Utils


class VirtualMouse:
    def __init__(self):
        self.image = None

    def recognize(self):
        image_test = True

        handprocess = handProcess.HandProcess(False, 1)
        utils = Utils()

        fpsTime = time.time()
        cap = cv2.VideoCapture(0)
        # 自动获取分辨率
        resize_w = screenInfo.screenInfo.get_w(screenInfo)
        resize_h = screenInfo.screenInfo.get_h(screenInfo)

        screenWidth = screenInfo.screenInfo.get_w(screenInfo)
        screenHeight = screenInfo.screenInfo.get_h(screenInfo)

        # 鼠标移动柔化和处理参数
        stepX, stepY = 0, 0
        smoothening = 7

        mouseDown = False

        while cap.isOpened():
            action_zh = ''
            success, self.image = cap.read()
            self.image = cv2.resize(self.image, (resize_w, resize_h))
            if not success:
                print("空帧")
                continue

            # 相关参数
            self.image.flags.writeable = False
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.image = cv2.flip(self.image, 1)
            self.image = handprocess.processOneHand(self.image)

            # 获取动作
            self.image, action, key_point = handprocess.checkHandAction(self.image, drawKeyFinger=True)
            action_zh = handprocess.action_labels[action]

            # 操作映射
            limit_x = screenInfo.screenInfo.get_w(screenInfo) / 1.5
            limit_y = screenInfo.screenInfo.get_h(screenInfo) / 1.5
            if key_point:
                action_trigger_time = 0

                # 映射距离
                x3 = np.interp(key_point[0], (0, resize_w), (0, screenWidth))
                y3 = np.interp(key_point[1], (0, resize_h), (0, screenHeight))

                # 柔和处理
                finalX = stepX + (x3 - stepX) / smoothening
                finalY = stepY + (y3 - stepY) / smoothening

                now = time.time()

                if action_zh == '夹住':
                    if not mouseDown:
                        pyautogui.mouseDown(button='left')
                        mouseDown = True
                    if 1 < finalX < limit_x and 1 < finalY < limit_y:
                        autopy.mouse.move(finalX, finalY)
                else:

                    if mouseDown:
                        pyautogui.mouseUp(button='left')

                    mouseDown = False

                if action_zh == '操作光标':
                    if 1 < finalX < limit_x and 1 < finalY < limit_y:
                        autopy.mouse.move(finalX, finalY)

                if action_zh == '触发单击' and (now - action_trigger_time > 0.3):
                    pyautogui.click()
                    action_trigger_time = now

                if action_zh == '退出':
                    exit()

                stepX, stepY = finalX, finalY

            self.image.flags.writeable = True
            self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)

            # 显示刷新率FPS
            cTime = time.time()
            fps_text = 1 / (cTime - fpsTime)
            fpsTime = cTime

            self.image = utils.cv2AddChineseText(self.image, "帧率: " + str(int(fps_text)), (10, 30),
                                                 textColor=(0, 255, 0), textSize=50)

            # 测试画面
            self.image = cv2.resize(self.image, (resize_w // 2, resize_h // 2))
            if image_test:
                cv2.imshow('Air Cursor (ver-alpha0.1.5)', self.image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()


# 开始程序
control = VirtualMouse()
control.recognize()
