import os
os.environ["GDK_BACKEND"] = "x11"

import time
import math
import tkinter as tk
from pathlib import Path

import numpy as np
import mujoco
import mujoco.viewer

# ===== 1. 加载模型 =====
path = Path(__file__).parent / "robot6.xml"
model = mujoco.MjModel.from_xml_path(str(path))
data = mujoco.MjData(model)
ik_data = mujoco.MjData(model)

site_id = model.site("end_effector").id

joint_names = [f"joint{i}" for i in range(1, 7)]
qids = [model.joint(n).qposadr[0] for n in joint_names]
dids = [model.joint(n).dofadr[0] for n in joint_names]

mujoco.mj_forward(model, ik_data)

# 初始末端位姿，作为滑块的零点
p0 = ik_data.site_xpos[site_id].copy()
R0 = ik_data.site_xmat[site_id].reshape(3, 3).copy()
q_target = np.zeros(6)

# ===== 2. 创建控制面板 =====
root = tk.Tk()
root.title("六自由度末端位姿 IK")
root.geometry("470x620")

tk.Label(
    root,
    text="6D Jacobian IK 控制面板",
    font=("Arial", 15, "bold")
).pack(pady=10)

def create_slider(name, lo, hi):
    s = tk.Scale(
        root, label=name,
        from_=lo, to=hi,
        resolution=1,
        orient=tk.HORIZONTAL,
        length=380
    )
    s.set(0)
    s.pack(pady=4)
    return s

# 位移：相对于初始位置，单位 cm
sx = create_slider("X 位移 (cm)", -15, 15)
sy = create_slider("Y 位移 (cm)", -15, 15)
sz = create_slider("Z 位移 (cm)", -15, 15)

# 姿态：相对于初始姿态，单位 度
sr = create_slider("Roll (度)", -45, 45)
sp = create_slider("Pitch (度)", -45, 45)
sw = create_slider("Yaw (度)", -45, 45)

info = tk.Label(root, text="准备就绪")
info.pack(pady=10)

running = True

def close_window():
    global running
    running = False

root.protocol("WM_DELETE_WINDOW", close_window)

def reset():
    for s in [sx, sy, sz, sr, sp, sw]:
        s.set(0)

tk.Button(
    root, text="目标复位",
    command=reset
).pack(pady=5)

# ===== 3. 欧拉角转旋转矩阵 =====
def euler_to_matrix(roll, pitch, yaw):
    cr, sr_ = math.cos(roll), math.sin(roll)
    cp, sp_ = math.cos(pitch), math.sin(pitch)
    cy, sy_ = math.cos(yaw), math.sin(yaw)

    Rx = np.array([
        [1, 0, 0],
        [0, cr, -sr_],
        [0, sr_, cr]
    ])
    Ry = np.array([
        [cp, 0, sp_],
        [0, 1, 0],
        [-sp_, 0, cp]
    ])
    Rz = np.array([
        [cy, -sy_, 0],
        [sy_, cy, 0],
        [0, 0, 1]
    ])
    return Rz @ Ry @ Rx

# ===== 4. 雅可比 IK =====
jacp = np.zeros((3, model.nv))
jacr = np.zeros((3, model.nv))

damping = 0.10
max_dq = 0.02

with mujoco.viewer.launch_passive(model, data) as viewer:

    while viewer.is_running() and running:
        try:
            root.update()
        except tk.TclError:
            break

        # 位置目标
        target_p = p0 + np.array([
            sx.get(), sy.get(), sz.get()
        ]) / 100.0

        # 姿态目标
        r, p, y = [
            math.radians(s.get())
            for s in (sr, sp, sw)
        ]
        target_R = euler_to_matrix(r, p, y) @ R0

        # 在独立的运动学数据中计算
        ik_data.qpos[qids] = q_target
        mujoco.mj_forward(model, ik_data)

        current_p = ik_data.site_xpos[site_id].copy()
        current_R = ik_data.site_xmat[
            site_id
        ].reshape(3, 3).copy()

        # 平移误差
        ep = target_p - current_p

        # 姿态误差（小角度近似）
        er = 0.5 * (
            np.cross(current_R[:, 0], target_R[:, 0])
            + np.cross(current_R[:, 1], target_R[:, 1])
            + np.cross(current_R[:, 2], target_R[:, 2])
        )

        error = np.concatenate([ep, er])

        # 6×6 末端雅可比矩阵
        mujoco.mj_jacSite(
            model, ik_data, jacp, jacr, site_id
        )
        J = np.vstack([
            jacp[:, dids],
            jacr[:, dids]
        ])

        # 阻尼最小二乘求关节增量
        A = J @ J.T + damping**2 * np.eye(6)
        dq = J.T @ np.linalg.solve(A, error)

        dq = np.clip(dq, -max_dq, max_dq)
        q_target += dq

        # 演示阶段使用软件关节角限制
        q_target = np.clip(
            q_target, -math.pi / 2, math.pi / 2
        )

        # 发送六个关节目标角度
        data.ctrl[:6] = q_target

        mujoco.mj_step(model, data)
        viewer.sync()

        actual_p = data.site_xpos[site_id]
        pos_err = np.linalg.norm(target_p - actual_p)

        info.config(
            text=f"实际末端位置: "
                 f"{np.round(actual_p, 3)}\n"
                 f"位置误差: {pos_err:.4f} m"
        )

        time.sleep(model.opt.timestep)

root.destroy()
