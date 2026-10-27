import mujoco
import mujoco.viewer
import numpy as np
import math
import time
from pathlib import Path

# 1. 加载机械臂
model_path = Path(__file__).parent / "robot.xml"
model = mujoco.MjModel.from_xml_path(str(model_path))
data = mujoco.MjData(model)

# 2. 设定末端目标位置
# 根据当前机械臂几何结构，构造一个可到达的坐标
target_x = (0.4 + 0.35 * math.cos(0.4)) * math.cos(0.5)
target_y = (0.4 + 0.35 * math.cos(0.4)) * math.sin(0.5)
target_z = 0.2 + 0.35 * math.sin(0.4)

print("目标位置：", target_x, target_y, target_z)

# 3. 逆运动学：由末端坐标求关节角度
radius = math.sqrt(target_x**2 + target_y**2)

joint1 = math.atan2(target_y, target_x)
joint2 = math.atan2(0.2 - target_z, radius - 0.4)

print("关节1目标角度：", math.degrees(joint1), "度")
print("关节2目标角度：", math.degrees(joint2), "度")

# 4. 运行 MuJoCo
with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():

        # 位置执行器接收 IK 计算出的角度
        data.ctrl[0] = joint1
        data.ctrl[1] = joint2

        mujoco.mj_step(model, data)
        viewer.sync()

        time.sleep(model.opt.timestep)
