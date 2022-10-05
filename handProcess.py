import time

import cv2
import mediapipe as mp
import math
from utils import Utils


class HandProcess:

    def __init__(self, static_image_mode=False, max_num_hands=2):
        # 参数
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=static_image_mode,
                                         min_detection_confidence=0.7,
                                         min_tracking_confidence=0.5,
                                         max_num_hands=max_num_hands)

        self.landmark_list = []

        self.action_labels = {
            'none': '无操作',
            'move': '操作光标',
            'click_single_ready': '单击准备',
            'click_single_active': '触发单击',
            'clamp_ready': '准备夹住',
            'clamp': '夹住',
            'exit': '退出',
        }
        self.action_deteted = ''

    # 检查左右手在数组中的index
    def checkHandsIndex(self, handedness):
        # 判断数量
        if len(handedness) == 1:
            handedness_list = [handedness[0].classification[0].label]
        else:
            handedness_list = [handedness[0].classification[0].label, handedness[1].classification[0].label]

        return handedness_list

    # 计算两点点的距离
    def getDistance(self, pointA, pointB):
        return math.hypot((pointA[0] - pointB[0]), (pointA[1] - pointB[1]))

    # 获取坐标
    def getFingerXY(self, index):
        return (self.landmark_list[index][1], self.landmark_list[index][2])

    # 绘制相关点
    def drawInfo(self, img, action):
        thumbXY, indexXY, middleXY = map(self.getFingerXY, [4, 8, 12])

        if action == 'move':
            img = cv2.circle(img, indexXY, 20, (0, 0, 255), -1)

        elif action == 'click_single_active':
            middle_point = int((indexXY[0] + thumbXY[0]) / 2), int((indexXY[1] + thumbXY[1]) / 2)
            img = cv2.circle(img, middle_point, 30, (0, 255, 0), -1)

        elif action == 'click_single_ready':
            img = cv2.circle(img, indexXY, 20, (255, 0, 0), -1)
            img = cv2.circle(img, thumbXY, 20, (255, 0, 0), -1)
            img = cv2.line(img, indexXY, thumbXY, (255, 0, 0), 2)


        elif action == 'clamp':
            middle_point = int((indexXY[0] + middleXY[0]) / 2), int((indexXY[1] + middleXY[1]) / 2)
            img = cv2.circle(img, middle_point, 30, (0, 255, 0), -1)

        elif action == 'clamp_ready':
            img = cv2.circle(img, indexXY, 20, (255, 0, 0), -1)
            img = cv2.circle(img, middleXY, 20, (255, 0, 0), -1)
            img = cv2.line(img, indexXY, middleXY, (255, 0, 0), 2)
        return img

    def checkHandAction(self, img, drawKeyFinger=True):
        upList = self.checkFingersUp()
        action = 'none'

        if len(upList) == 0:
            return img, action, None

        # 侦测距离
        dete_dist = 100
        # 中指
        key_point = self.getFingerXY(8)

        # 移动模式：单个食指在上，鼠标跟随食指指尖移动，需要smooth处理防抖
        if (upList == [0, 1, 0, 0, 0]):
            action = 'move'

        # 单击：食指与拇指出现暂停移动，如果两指捏合，触发单击
        if (upList == [1, 1, 0, 0, 0]):
            l1 = self.getDistance(self.getFingerXY(4), self.getFingerXY(8))
            action = 'click_single_active' if l1 < dete_dist else 'click_single_ready'

        # 夹住：食指、中指出现暂停移动，如果两指捏合，触发夹住
        if (upList == [0, 1, 1, 0, 0]):
            l1 = self.getDistance(self.getFingerXY(8), self.getFingerXY(12))
            action = 'clamp' if l1 < dete_dist else 'clamp_ready'

        # 退出：五指向上
        if (upList == [1, 1, 1, 1, 1]):
            action = 'exit'

        # 根据动作绘制相关点
        img = self.drawInfo(img, action) if drawKeyFinger else img

        self.action_deteted = self.action_labels[action]

        return img, action, key_point

    # 返回向上手指的数组
    def checkFingersUp(self):

        fingerTipIndexs = [4, 8, 12, 16, 20]
        upList = []
        if len(self.landmark_list) == 0:
            return upList

        # 拇指，比较x坐标
        if self.landmark_list[fingerTipIndexs[0]][1] < self.landmark_list[fingerTipIndexs[0] - 1][1]:
            upList.append(1)
        else:
            upList.append(0)

        # 其他指头，比较Y坐标
        for i in range(1, 5):
            if self.landmark_list[fingerTipIndexs[i]][2] < self.landmark_list[fingerTipIndexs[i] - 2][2]:
                upList.append(1)
            else:
                upList.append(0)

        return upList

    # 分析手
    def processOneHand(self, img, drawlabel=True, drawLandmarks=True):
        utils = Utils()

        results = self.hands.process(img)
        self.landmark_list = []

        if results.multi_hand_landmarks:

            for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):

                if drawLandmarks:
                    self.mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style())

                for landmark_id, finger_axis in enumerate(hand_landmarks.landmark):
                    h, w, c = img.shape
                    p_x, p_y = math.ceil(finger_axis.x * w), math.ceil(finger_axis.y * h)

                    self.landmark_list.append([
                        landmark_id, p_x, p_y,
                        finger_axis.z
                    ])

                if drawlabel:
                    x_min, x_max = min(self.landmark_list, key=lambda i: i[1])[1], \
                                   max(self.landmark_list, key=lambda i: i[1])[1]
                    y_min, y_max = min(self.landmark_list, key=lambda i: i[2])[2], \
                                   max(self.landmark_list, key=lambda i: i[2])[2]

                    img = utils.cv2AddChineseText(img, self.action_deteted, (x_min, y_min),
                                                  textColor=(0, 0, 255), textSize=60)
                    if(self.action_deteted=='退出'):
                        time.sleep(1)

        return img
