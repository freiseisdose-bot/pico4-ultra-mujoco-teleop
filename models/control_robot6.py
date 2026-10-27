import os

# 沿用之前解决图形窗口报错的方法
os.environ["GDK_BACKEND"] = "x11"

import mujoco
import mujoco.viewer
import tkinter as tk
import math
import time
from pathlib import Path

# ===== 1. 加载六自由度机械臂 =====
model_path = Path(__file__).parent / "robot6.xml"

model = mujoco.MjModel.from_xml_path(str(model_path))
data = mujoco.MjData(model)

print("模型加载成功！")
print("自由度数量：", model.nv)
print("执行器数量：", model.nu)

# ===== 2. 创建控制面板 =====
root = tk.Tk()
root.title("六自由度机械臂控制系统")
root.geometry("470x600")

title = tk.Label(
    root,
    text="MuJoCo 六自由度机械臂控制",
    font=("Arial", 15, "bold")
)
title.pack(pady=12)

sliders = []

for i in range(6):
    slider = tk.Scale(
        root,
        from_=-90,
        to=90,
        resolution=1,
        orient=tk.HORIZONTAL,
        length=380,
        label=f"Joint {i+1} (度)"
    )
    slider.set(0)
    slider.pack(pady=5)
    sliders.append(slider)

status = tk.Label(
    root,
    text="准备控制机械臂",
    font=("Arial", 11)
)
status.pack(pady=10)

running = True

def close_panel():
    global running
    running = False

root.protocol("WM_DELETE_WINDOW", close_panel)

def reset_joints():
    for slider in sliders:
        slider.set(0)

reset_button = tk.Button(
    root,
    text="关节归零",
    command=reset_joints
)
reset_button.pack(pady=5)

# ===== 3. MuJoCo 运行循环 =====
with mujoco.viewer.launch_passive(model, data) as viewer:

    while viewer.is_running() and running:
        try:
            root.update()
        except tk.TclError:
            break

        # 读取六个滑块的目标角度
        for i in range(6):
            angle_deg = sliders[i].get()
            angle_rad = math.radians(angle_deg)

            # 六个位置执行器分别控制六个关节
            data.ctrl[i] = angle_rad

        # 物理仿真
        mujoco.mj_step(model, data)

        # 更新窗口
        viewer.sync()

        time.sleep(model.opt.timestep)

root.destroy()
