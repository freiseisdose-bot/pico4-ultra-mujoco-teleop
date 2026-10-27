# PICO 4 Ultra × MuJoCo 机械臂遥操作

在 Ubuntu 上学习机械臂仿真、逆运动学与 VR 遥操作。

**当前阶段：** 已归档双关节与六关节控制、雅可比 IK；开始 UDP 通信测试，PICO 实机尚未接入。

## 代码

| 阶段 | 文件 |
| --- | --- |
| 双关节入门 | models/robot.xml、control.py、joint_slider.py |
| 双关节解析 IK | models/ik_control.py（固定目标）、ik_position_slider.py（XY 滑块） |
| 双关节数值 IK | models/jacobian_ik.py |
| 六关节模型与控制 | models/robot6.xml、control_robot6.py |
| 六自由度位姿 IK | models/ik_robot6.py |
| UDP 本机测试 | pico/pico_receiver.py、test_pico_sender.py |

上述模型相关脚本均在 models/ 内，使用同目录 XML。保留新对话代码原文，只整理文件位置与首尾空行。

## 运行

使用装有 MuJoCo、NumPy、tkinter 的 Python 桌面环境。在仓库根目录选择一个程序运行，也可用 VS Code 的运行按钮：

```bash
python models/control_robot6.py
python models/ik_robot6.py
```

UDP 测试需要两个终端：先运行接收器，再运行模拟发送器。

```bash
python pico/pico_receiver.py
python pico/test_pico_sender.py
```

发送地址为 127.0.0.1，端口为 5005；接收器目前只打印位姿，尚未驱动机械臂。

## 使用说明

- joint_slider.py 控制关节角；ik_robot6.py 控制末端位置和姿态目标。
- 双关节只有两个自由度，无法独立满足任意 XYZ；XY 解析版本还可能产生低于地面的目标。
- 六关节模型暂时关闭重力；IK 是演示版本，目标不一定可达，姿态误差采用局部近似。
- 六关节脚本保留对话中的 X11 设置。双关节 joint_slider.py 退出时先关闭 MuJoCo 窗口。

## 验证与下一步

本次新增 6 个 Python 文件通过语法检查，六关节 XML 通过结构检查；**原始 UDP 发送器和接收器已在整理环境中通过本机收发测试**。尚未重跑 MuJoCo 图形仿真或 PICO 实机测试。

下一步：PICO 真实位姿发送 → 坐标标定 → 接入六自由度 IK → 遥操作联调。

来源：[最新项目对话](https://chatgpt.com/share/6ae09aa6-1e4c-83ee-bd93-f9a5c9ea409e)。早期版本与精简前内容可从 Git 历史恢复。
