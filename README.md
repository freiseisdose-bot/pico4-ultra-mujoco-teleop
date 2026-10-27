# PICO 4 Ultra + MuJoCo 机械臂遥操作

基于 Ubuntu Linux，逐步实现 PICO 4 Ultra 驱动 MuJoCo 仿真机械臂的学习与实验项目。

**当前阶段：基础仿真与解析逆运动学。PICO 数据接入与完整遥操作闭环尚未完成。**

## 已归档代码

代码从用户提供的「项目技术路线」分享对话中提取；2026-10-27 完成整理。保留历史命名，统一把相互依赖的实验脚本和模型放在 models/。

| 文件 | 作用 | 状态 |
| --- | --- | --- |
| [models/robot.xml](models/robot.xml) | 双关节机械臂、位置执行器、末端 site | 按原对话修正 site 层级 |
| [models/control.py](models/control.py) | 两关节正弦/余弦自动运动 | 按原对话修正模型路径 |
| [models/slider_control.py](models/slider_control.py) | 较慢的自动轨迹 | 历史名称；实际没有滑块 |
| [models/keyboard_control.py](models/keyboard_control.py) | WASD 调整关节目标角度 | 保留实验原版；与 Viewer 快捷键存在冲突 |
| [models/ik_control.py](models/ik_control.py) | 当前 yaw/pitch 两关节模型的解析 IK | 固定可达目标，不是通用六轴 IK |
| [models/ik_slider.py](models/ik_slider.py) | Tkinter 关节角滑块 | 控制关节角，不是末端坐标 IK |
| [reference/pico_receiver.py](reference/pico_receiver.py) | UDP JSON 接收教学示例 | 未验证 PICO 实机联通 |
| [reference/ControllerReader.cs](reference/ControllerReader.cs) | Unity XR 手柄位姿读取示例 | 只输出日志，没有发送 UDP |
| [archive/historical-code.md](archive/historical-code.md) | 初始模型、历史控制代码和修改片段 | 原文归档，含已知问题 |
| [examples/launch_viewer.py](examples/launch_viewer.py) | 早期查看器启动片段 | 在 models 目录运行或自行提供 robot.xml |

## 在已有 Ubuntu 环境中运行

使用之前已安装 MuJoCo 的 Python 环境。从仓库根目录选择一项运行：

```bash
python models/control.py
python models/slider_control.py
python models/ik_control.py
python models/ik_slider.py
```

一次运行一个脚本。VS Code 也可以打开相应文件，选择已安装 MuJoCo 的 Python 解释器后运行。

依赖：MuJoCo；ik_control.py 还保留原文中的 NumPy 导入；滑块程序需要 Python 的 tkinter 和桌面图形环境。此前环境记录为 MuJoCo 3.1.7，完整版本锁定尚未取得。

为保留原实现，脚本未增加额外的 GUI 生命周期处理。运行 ik_slider.py 时建议先关闭 MuJoCo 窗口；先关闭 Tkinter 面板可能使 root.update() 报错。

## 当前成果与限制

- 已安装并进入 Ubuntu；此前已启动 MuJoCo、加载机械臂模型。
- 已开展自动控制和键盘控制实验；键盘与 Viewer 快捷键冲突已记录。
- 已提供与当前机械臂结构匹配的解析 IK 示例，正在学习雅可比与数值 IK。
- 分享对话没有 jacobian_ik.py 或 ik_test.py，待取得对应「学习运动步骤」对话后归档。
- 关节 1 绕 Z 轴、关节 2 绕 Y 轴，不能套用普通共面双连杆公式。
- 位置执行器控制受重力、接触与增益影响；几何 IK 精确不代表仿真末端零误差。
- reference/ 中两个教学片段尚未组成完整采集通信系统；接收器的超时分支只打印提示，并不实际停止机器人。

## 本次验证

6 个 Python 文件通过语法解析；XML 通过结构检查，末端 site 位于 link2 内；解析 IK 固定目标经对应正运动学回代，计算误差为 0.0（浮点结果）。

当前整理环境没有 MuJoCo，未重新运行物理仿真、桌面窗口或 Unity/PICO 实机测试。不能把静态检查当成完整运行验证。

详细来源、改动和验证范围见 [代码恢复记录](docs/code-recovery.md)。

## 后续计划

1. 在原 Ubuntu 环境运行归档代码，保存截图、录像、环境版本和末端误差。
2. 归档并验证雅可比与阻尼最小二乘 IK 示例。
3. 验证 PICO 位姿采集与 Ubuntu 数据接收。
4. 完成坐标系转换、初始位姿标定与运动比例设置。
5. 接入目标机械臂，加入关节限位、速度限制和失联暂停，完成遥操作联调。

目标流程：PICO 位姿 → Ubuntu 接收 → 坐标映射与标定 → 末端目标 → IK → 关节控制 → MuJoCo 反馈。

## 参考项目

[qqsq12321/vr_teleop](https://github.com/qqsq12321/vr_teleop) 是此前学习参考，本次未复制其源码。采用第三方代码时应记录来源并遵守其许可证。
