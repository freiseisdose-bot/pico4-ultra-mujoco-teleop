# 分享对话中的历史代码原文

仅保存代码，不代表最终版本或均已运行成功。代码块去掉首尾空行，正文未修改。

## 初始模型

```xml
<mujoco model="my_first_robot">
  <option gravity="0 0 -9.81"/>

  <worldbody>
    <geom type="plane" size="2 2 0.1"
          rgba="0.8 0.8 0.8 1"/>

    <body name="link1" pos="0 0 0.2">
      <joint name="joint1" type="hinge"
             axis="0 0 1" damping="1"/>
      <geom type="capsule"
            fromto="0 0 0 0.4 0 0"
            size="0.05" mass="1"
            rgba="0.2 0.5 0.9 1"/>

      <body name="link2" pos="0.4 0 0">
        <joint name="joint2" type="hinge"
               axis="0 1 0" damping="1"/>
        <geom type="capsule"
              fromto="0 0 0 0.35 0 0"
              size="0.04" mass="0.5"
              rgba="0.9 0.4 0.2 1"/>
      </body>
    </body>
  </worldbody>

  <actuator>
    <position joint="joint1" kp="100"/>
    <position joint="joint2" kp="100"/>
  </actuator>
</mujoco>
```

## VS Code 自动控制（原始路径）

```python
import mujoco
import mujoco.viewer
import math
import time
from pathlib import Path

# 自动定位机械臂模型
model_path = Path(__file__).parent / "models" / "robot.xml"

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
```

## 初版硬编码路径控制

```python
import mujoco
import mujoco.viewer
import time
import math

# 1. 加载机械臂模型
model = mujoco.MjModel.from_xml_path(
    "/home/a1111/robot_vr_project/models/robot.xml"
)
data = mujoco.MjData(model)

# 2. 打开 MuJoCo 仿真窗口
with mujoco.viewer.launch_passive(model, data) as viewer:

    start_time = time.time()

    while viewer.is_running():

        # 3. 计算两个关节的目标角度
        t = time.time() - start_time

        data.ctrl[0] = 0.5 * math.sin(t)
        data.ctrl[1] = 0.5 * math.cos(t)

        # 4. 推进物理仿真
        mujoco.mj_step(model, data)

        # 5. 更新显示
        viewer.sync()

        time.sleep(model.opt.timestep)
```

## IJKL 按键修改片段

```python
def key_callback(key):
    if key == 73:       # I
        target[0] += step
    elif key == 75:     # K
        target[0] -= step
    elif key == 74:     # J
        target[1] += step
    elif key == 76:     # L
        target[1] -= step

    print("目标关节角度:", target)
```

## 用户粘贴的模型（site 层级未修正）

```xml
<mujoco model="my_first_robot">
  <option gravity="0 0 -9.81"/>

  <worldbody>
    <geom type="plane" size="2 2 0.1"
          rgba="0.8 0.8 0.8 1"/>

    <body name="link1" pos="0 0 0.2">
      <joint name="joint1" type="hinge"
             axis="0 0 1" damping="1"/>
      <geom type="capsule"
            fromto="0 0 0 0.4 0 0"
            size="0.05" mass="1"
            rgba="0.2 0.5 0.9 1"/>

      <body name="link2" pos="0.4 0 0">
        <joint name="joint2" type="hinge"
               axis="0 1 0" damping="1"/>
        <geom type="capsule"
              fromto="0 0 0 0.35 0 0"
              size="0.04" mass="0.5"
              rgba="0.9 0.4 0.2 1"/>
      </body>
   <site name="end_effector"
      pos="0.35 0 0"
      size="0.025"
      rgba="0 1 0 1"/>
    </body>
  </worldbody>

  <actuator>
    <position joint="joint1" kp="100"/>
    <position joint="joint2" kp="100"/>
  </actuator>
</mujoco>
```
