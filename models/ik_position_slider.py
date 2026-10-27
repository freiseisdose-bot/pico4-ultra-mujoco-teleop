import math
import time
import tkinter as tk
from pathlib import Path

import mujoco
import mujoco.viewer

# 1. 加载机械臂模型
model_path = Path(__file__).parent / "robot.xml"
model = mujoco.MjModel.from_xml_path(str(model_path))
data = mujoco.MjData(model)

# 机械臂参数（单位：米）
L1 = 0.40
L2 = 0.35
BASE_HEIGHT = 0.20

site_id = model.site("end_effector").id

# 2. 创建控制面板
root = tk.Tk()
root.title("机械臂逆运动学 IK 控制")
root.geometry("430x320")

x_slider = tk.Scale(
    root, from_=0.10, to=0.75,
    resolution=0.01,
    orient=tk.HORIZONTAL,
    length=360,
    label="目标 X (米)"
)
x_slider.set(0.65)
x_slider.pack(pady=8)

y_slider = tk.Scale(
    root, from_=-0.60, to=0.60,
    resolution=0.01,
    orient=tk.HORIZONTAL,
    length=360,
    label="目标 Y (米)"
)
y_slider.set(0.15)
y_slider.pack(pady=8)

status = tk.Label(root, text="准备就绪")
status.pack(pady=8)

position_label = tk.Label(root, text="")
position_label.pack(pady=5)

running = True

def close_panel():
    global running
    running = False

root.protocol("WM_DELETE_WINDOW", close_panel)

# 3. 逆运动学计算
def inverse_kinematics(x, y):
    r = math.hypot(x, y)

    # 当前机械臂的水平可达距离
    if r < L1 - 1e-6 or r > L1 + L2 + 1e-6:
        return None

    # 第一个关节：绕 Z 轴旋转
    q1 = math.atan2(y, x)

    # 第二个关节：绕局部 Y 轴旋转
    cos_q2 = (r - L1) / L2
    cos_q2 = max(-1.0, min(1.0, cos_q2))
    q2 = math.acos(cos_q2)

    # 由第二个关节角度确定高度
    z = BASE_HEIGHT - L2 * math.sin(q2)

    return q1, q2, z

# 4. 启动 MuJoCo
with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running() and running:

        root.update()

        x = float(x_slider.get())
        y = float(y_slider.get())

        result = inverse_kinematics(x, y)

        if result is not None:
            q1, q2, target_z = result

            data.ctrl[0] = q1
            data.ctrl[1] = q2

            status.config(
                text=f"目标角度：{math.degrees(q1):.1f}°，"
                     f"{math.degrees(q2):.1f}°"
            )
        else:
            status.config(
                text="目标超出当前机械臂的可达范围",
                fg="red"
            )

        mujoco.mj_step(model, data)

        # 读取实际末端坐标
        px, py, pz = data.site_xpos[site_id]
        position_label.config(
            text=f"实际末端：X={px:.3f}  "
                 f"Y={py:.3f}  Z={pz:.3f}"
        )

        viewer.sync()
        time.sleep(model.opt.timestep)

if running:
    root.destroy()
