# Air_Cursor
基于mediapipe的手势识别光标

# ——环境搭建 
依赖表：

依赖名称 | 版本
-|-
Python | 3.8.13
mediapipe | 0.8.9
autopy | 4.0.0
opencv-python | 4.5.5.64
pywin32 | 225
PyAutoGUI | 0.9.53

建议使用 anaconda 安装搭建虚拟环境运行本项目，本说明仅提供使用 anaconda 搭建环境
的教程，强烈建议按照下述步骤进行安装。如果不想使用 anaconda，可以参考上面的依赖
表自行搭建环境。

# 步骤一：安装 anaconda

1 解压/完整项目以及使用说明/在 anaconda 官网下载安装程序

2 双击按照弹窗提示安装 Anaconda3-2021.11-Windows-x86_64.exe

![image](https://user-images.githubusercontent.com/81380030/194018140-030940b0-cb8b-4aac-98de-a03b2211de64.png)


# 步骤二：安装空气光标（Air Cursor）的环境依赖

1 解压/Air_Cursor ver0.1.5(alpha)/并放置于英文路径下
![image](https://user-images.githubusercontent.com/81380030/194018233-c41bd39c-beb4-404e-b796-cf1aaf71983c.png)

2 打开命令提示符 cmd，建议直接在路径栏输入 cmd，如图所示
![image](https://user-images.githubusercontent.com/81380030/194018255-4fbecd38-c392-431c-877a-9da01edff961.png)

3 输入 conda env create -f environment.yml 回车，完成后如图所示
![image](https://user-images.githubusercontent.com/81380030/194018286-284c4127-215f-4eb7-8cea-5b115cd62454.png)

4 输入 conda info –-envs，出现环境 Air-Cursor，代表安装成功。
![image](https://user-images.githubusercontent.com/81380030/194018303-d17447a1-9afe-42ad-ab93-3740f99ae206.png)
