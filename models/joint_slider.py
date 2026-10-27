import mujoco
import mujoco.viewer
import tkinter as tk
from pathlib import Path

model_path = Path(__file__).parent / "robot.xml"
model = mujoco.MjModel.from_xml_path(str(model_path))
data = mujoco.MjData(model)

# 先使用关节角度滑块验证控制面板
root = tk.Tk()
root.title("MuJoCo 机械臂控制面板")
root.geometry("380x240")

joint1 = tk.Scale(
    root, from_=-90, to=90,
    orient=tk.HORIZONTAL,
    length=320, label="关节 1 (度)"
)
joint1.pack(pady=10)

joint2 = tk.Scale(
    root, from_=-60, to=60,
    orient=tk.HORIZONTAL,
    length=320, label="关节 2 (度)"
)
joint2.pack(pady=10)

import math
import time

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        root.update()

        data.ctrl[0] = math.radians(joint1.get())
        data.ctrl[1] = math.radians(joint2.get())

        mujoco.mj_step(model, data)
        viewer.sync()
        time.sleep(model.opt.timestep)

root.destroy()
