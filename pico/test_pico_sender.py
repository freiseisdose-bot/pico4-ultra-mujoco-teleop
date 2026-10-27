import socket
import json
import math
import time

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

print("开始模拟 PICO 手柄数据...")

try:
    while True:
        t = time.time()

        message = {
            "position": {
                "x": 0.3 + 0.1 * math.sin(t),
                "y": 0.2,
                "z": 0.4
            },
            "rotation": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            }
        }

        data = json.dumps(message).encode("utf-8")

        sock.sendto(
            data,
            ("127.0.0.1", 5005)
        )

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    sock.close()
