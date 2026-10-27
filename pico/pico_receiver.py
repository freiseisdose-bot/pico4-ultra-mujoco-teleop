import socket
import json

# 创建 UDP 接收器
sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

# 接收所有网卡发来的数据
sock.bind(("0.0.0.0", 5005))
sock.settimeout(1.0)

print("PICO 数据接收器已启动")
print("监听 UDP 端口：5005")
print("等待 PICO 手柄数据...")

try:
    while True:
        try:
            data, addr = sock.recvfrom(4096)
        except socket.timeout:
            continue

        try:
            message = json.loads(
                data.decode("utf-8")
            )

            position = message["position"]
            rotation = message["rotation"]

            print("\n收到数据，来自:", addr)
            print("位置:", position)
            print("姿态:", rotation)

        except (ValueError, KeyError, TypeError) as e:
            print("数据格式不正确:", e)

except KeyboardInterrupt:
    print("接收器已停止")

finally:
    sock.close()
