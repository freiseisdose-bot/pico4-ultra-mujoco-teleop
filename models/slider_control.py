import mujoco
import mujoco.viewer
import time
import math
from pathlib import Path

# 加载模型
model_path = Path(__file__).parent / "robot.xml"
model = mujoco.MjModel.from_xml_path(str(model_path))
data = mujoco.MjData(model)

# 启动仿真
with mujoco.viewer.launch_passive(model, data) as viewer:
    start_time = time.time()

    while viewer.is_running():
        t = time.time() - start_time

        # 两个关节自动缓慢运动
        data.ctrl[0] = 0.3 * math.sin(t * 0.5)
        data.ctrl[1] = 0.3 * math.cos(t * 0.5)

        mujoco.mj_step(model, data)
        viewer.sync()

        time.sleep(model.opt.timestep)
