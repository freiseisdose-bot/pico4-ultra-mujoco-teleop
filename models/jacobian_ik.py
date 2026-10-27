import mujoco
import mujoco.viewer
import numpy as np
import tkinter as tk
import time
from pathlib import Path

# 1. 加载机械臂
model_path = Path(__file__).parent / "robot.xml"
model = mujoco.MjModel.from_xml_path(str(model_path))
data = mujoco.MjData(model)

site_id = model.site("end_effector").id

# 2. 创建目标位置控制面板
root = tk.Tk()
root.title("Jacobian IK 机械臂控制")
root.geometry("430x340")

def add_slider(name, minimum, maximum, initial):
    slider = tk.Scale(
        root,
        from_=minimum,
        to=maximum,
        resolution=0.01,
        orient=tk.HORIZONTAL,
        length=360,
        label=name
    )
    slider.set(initial)
    slider.pack(pady=5)
    return slider

x_slider = add_slider("目标 X (m)", 0.10, 0.75, 0.65)
y_slider = add_slider("目标 Y (m)", -0.50, 0.50, 0.10)
z_slider = add_slider("目标 Z (m)", -0.10, 0.50, 0.10)

info = tk.Label(root, text="等待仿真...")
info.pack(pady=10)

running = True

def close_panel():
    global running
    running = False

root.protocol("WM_DELETE_WINDOW", close_panel)

# 3. 雅可比矩阵 IK 参数
jacp = np.zeros((3, model.nv))
jacr = np.zeros((3, model.nv))

# 阻尼最小二乘，缓解奇异位置的问题
damping = 0.05
gain = 0.5
max_step = 0.015

# 只使用当前两个关节
joint_ids = [
    model.joint("joint1").id,
    model.joint("joint2").id
]
dof_ids = [
    int(model.jnt_dofadr[j]) for j in joint_ids
]
qpos_ids = [
    int(model.jnt_qposadr[j]) for j in joint_ids
]

# 保存 IK 迭代使用的关节目标
q_target = data.qpos[qpos_ids].copy()

# 4. 打开 MuJoCo
with mujoco.viewer.launch_passive(model, data) as viewer:

    while viewer.is_running() and running:
        try:
            root.update()
        except tk.TclError:
            break

        target = np.array([
            x_slider.get(),
            y_slider.get(),
            z_slider.get()
        ], dtype=float)

        # 在独立的运动学状态中求解 IK，
        # 避免修改正在进行的物理仿真
        ik_data = mujoco.MjData(model)
        ik_data.qpos[qpos_ids] = q_target
        mujoco.mj_forward(model, ik_data)

        current = ik_data.site_xpos[site_id].copy()
        error = target - current

        # 计算末端位置雅可比矩阵
        mujoco.mj_jacSite(
            model, ik_data, jacp, jacr, site_id
        )
        J = jacp[:, dof_ids]

        # 阻尼最小二乘：
        # dq = J.T (J J.T + λ² I)^(-1) e
        A = J @ J.T + damping**2 * np.eye(3)
        dq = J.T @ np.linalg.solve(A, error)

        # 限制每次关节目标变化
        dq = np.clip(gain * dq, -max_step, max_step)
        q_target += dq

        # 输出给位置执行器
        data.ctrl[0] = q_target[0]
        data.ctrl[1] = q_target[1]

        mujoco.mj_step(model, data)
        viewer.sync()

        actual = data.site_xpos[site_id].copy()
        actual_error = np.linalg.norm(target - actual)

        info.config(
            text=f"末端误差: {actual_error:.3f} m\n"
                 f"实际位置: {np.round(actual, 3)}"
        )

        time.sleep(model.opt.timestep)

root.destroy()
