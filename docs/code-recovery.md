# 历史代码恢复记录

更新日期：2026-10-27。

## 来源与恢复方式

来源：[用户提供的「项目技术路线」分享对话](https://chatgpt.com/share/6ae062d4-9ff4-83e8-8d2a-6125162f7bdc)。

此前历史检索只返回摘要；本次成功取得分享页面内嵌的对话文本，提取完整代码块。只归档与项目有关的代码，没有上传整段聊天、账号信息或图片。

## 代码整理规则

- Python 和 C# 代码块去除 Markdown 围栏及首尾空行，保留原有实现。
- models/ 中各脚本与 robot.xml 同目录，沿用对话采用的文件组织。
- control.py 采用 VS Code 版本，并应用原对话后续路径修正：Path(__file__).parent / "robot.xml"。
- robot.xml 以用户粘贴的完整模型为基础，应用原对话的 site 修正：将 end_effector 移入 link2 内，保持 pos="0.35 0 0"。没有改变连杆长度、关节轴、质量或执行器增益。
- 历史未修正模型、初始无 site 模型、原始路径版本和 IJKL 回调片段保存在 archive/historical-code.md。
- reference/ 中接收器按用途命名为 pico_receiver.py；Unity 文件名依据 ControllerReader 类名。它们是教学示例，不代表已完成实机通信。

## 各文件对应的原对话内容

| 文件 | 来源内容 |
| --- | --- |
| models/robot.xml | 用户粘贴完整 XML，以及后续“末端标记放错位置”的修正 |
| models/control.py | VS Code 自动定位模型的控制程序，以及重复 models/models 路径修正 |
| models/slider_control.py | 解决 WASD/IJKL 与查看器冲突后的慢速自动轨迹 |
| models/keyboard_control.py | WASD 控制两个关节的完整程序 |
| models/ik_control.py | 构造可达三维目标并求 yaw/pitch 两个关节角的解析 IK |
| models/ik_slider.py | Tkinter 两个关节角滑块验证程序 |
| reference/pico_receiver.py | PICO 技术讲解中的 Ubuntu UDP 接收器示例 |
| reference/ControllerReader.cs | Unity XR 读取右手柄位姿和扳机并打印日志的示例 |

## 核对后的注意事项

1. slider_control.py 实际是自动轨迹，ik_slider.py 实际是关节角控制；文件名不代表已经实现末端 IK 滑块。
2. 模型关节轴为 Z、Y，解析 IK 与这种结构对应，不是标准共面双连杆公式。
3. keyboard_control.py 保留原版，Viewer 按键冲突仍存在；优先运行自动控制或 Tkinter 滑块。
4. Tkinter 窗口先关闭时可能引发更新错误；本次归档未重写窗口生命周期。
5. UDP 超时分支仅输出 “stop control” 文本，没有执行机器人停止动作。Unity 示例没有网络发送功能。
6. 原对话解析 IK 表格中的 Z 近似值与代码不完全一致，应以代码计算为准（约 0.3362964 m）。
7. 此分享不含 jacobian_ik.py、ik_test.py；它们仍需从另一份「学习运动步骤」对话恢复。

## 本次验证结果

- 5 个 models/ Python 文件和 reference/pico_receiver.py：Python AST 语法解析通过。
- XML：解析通过；确认两个关节、两个位置执行器及 end_effector 所属 link2。
- 解析 IK：按源码目标计算，所得关节角为 0.5 rad、-0.4 rad；经对应 yaw/pitch 正运动学回代，欧氏位置误差为 0.0。
- 未运行 MuJoCo 物理仿真、GUI、Unity 编译或 PICO 网络联调；当前整理环境没有 MuJoCo。
- GitHub 上传后核对文件内容。

这里的静态验证不代表原电脑上的最终文件或运行状态已被重新验证。
