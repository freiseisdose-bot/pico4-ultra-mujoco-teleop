import mujoco
import mujoco.viewer
import math
import time
from pathlib import Path

# 自动定位机械臂模型
model_path = Path(__file__).parent / "robot.xml"

model = mujoco.MjModel.from_xml_path(str(model_path))
data = mujoco.MjData(model)

# 启动 MuJoCo 可视化窗口
with mujoco.viewer.launch_passive(model, data) as viewer:
    start = time.time()

    while viewer.is_running():
        t = time.time() - start

        # 控制两个关节周期性运动
        data.ctrl[0] = 0.5 * math.sin(t)
        data.ctrl[1] = 0.5 * math.cos(t)

        mujoco.mj_step(model, data)
        viewer.sync()

        time.sleep(model.opt.timestep)
