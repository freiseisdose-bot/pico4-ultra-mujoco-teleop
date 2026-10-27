# 从历史对话检索返回的模型启动片段整理，仅将分号分隔语句换行。
# 运行时需要当前工作目录中存在原始 robot.xml；该模型尚未恢复。
import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("robot.xml")
data = mujoco.MjData(model)
mujoco.viewer.launch(model, data)
