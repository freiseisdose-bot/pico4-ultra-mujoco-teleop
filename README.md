# PICO 4 Ultra × MuJoCo 机械臂遥操作

在 Ubuntu 上学习机械臂仿真与控制，逐步接入 PICO 4 Ultra。

**当前进度：** 已完成基础模型与控制实验，正在学习逆运动学；PICO 遥操作尚未接通。

## 文件

| 文件 | 用途 |
| --- | --- |
| [models/robot.xml](models/robot.xml) | 双关节机械臂模型 |
| [models/control.py](models/control.py) | 自动往复运动 |
| [models/ik_control.py](models/ik_control.py) | 固定目标的解析逆运动学 |
| [models/joint_slider.py](models/joint_slider.py) | 用滑块调整两个关节角度 |

## 运行

使用已安装 MuJoCo 和 NumPy 的 Python 环境；滑块还需要 tkinter 和桌面环境。

在仓库根目录运行，三选一：

```bash
python models/control.py
python models/ik_control.py
python models/joint_slider.py
```

也可在 VS Code 中选择相应 Python 环境，打开脚本后点击运行。

- 滑块控制的是关节角，不是末端坐标；退出时先关闭 MuJoCo 窗口。
- IK 针对当前 Z/Y 轴两关节模型；实际仿真会受重力影响。

## 下一步

数值 IK → PICO 数据接收 → 坐标标定 → 遥操作联调。

代码来自[项目技术路线对话](https://chatgpt.com/share/6ae062d4-9ff4-83e8-8d2a-6125162f7bdc)。已做语法、XML 结构和 IK 回代检查，尚未在整理环境中重跑仿真。旧示例与归档说明保留在 Git 提交历史中。
