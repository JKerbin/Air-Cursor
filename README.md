# Air_Cursor
基于mediapipe的手势识别光标

## 环境搭建 
依赖表：

依赖名称 | 版本
-|-
Python | 3.8.13
mediapipe | 0.8.9
autopy | 4.0.0
opencv-python | 4.5.5.64
pywin32 | 225
PyAutoGUI | 0.9.53

建议使用anaconda配置对应环境

## 运行方法

- 解压/Air_Cursor ver0.1.5(alpha)/于英文路径中
- 安装对应环境
```bash
$ conda init
$ conda env create -f environment.yml
$ conda info –-envs
$ conda activate Air-Cursor
$ python main.py
# 出现INFO: Created TensorFlow Lite XNNPACK delegate for CPU.表示成功运行
```


