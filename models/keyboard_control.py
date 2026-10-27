import mujoco
import mujoco.viewer
import time
from pathlib import Path

# 加载机械臂模型
model_path = Path(__file__).parent / "robot.xml"
model = mujoco.MjModel.from_xml_path(str(model_path))
data = mujoco.MjData(model)

# 两个关节的目标角度（弧度）
target = [0.0, 0.0]
step = 0.1

def key_callback(key):
    # GLFW 键盘按键编码
    if key == 87:       # W
        target[0] += step
    elif key == 83:     # S
        target[0] -= step
    elif key == 65:     # A
        target[1] += step
    elif key == 68:     # D
        target[1] -= step

    print("目标关节角度:", target)

# 启动仿真
with mujoco.viewer.launch_passive(
    model, data, key_callback=key_callback
) as viewer:

    while viewer.is_running():
        data.ctrl[0] = target[0]
        data.ctrl[1] = target[1]

        mujoco.mj_step(model, data)
        viewer.sync()

        time.sleep(model.opt.timestep)
