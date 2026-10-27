import socket
import json
import time

HOST = "0.0.0.0"
PORT = 5005

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.bind((HOST, PORT))
sock.settimeout(0.2)

print(f"Waiting for PICO data on UDP {PORT}")

last_packet_time = None

while True:
    try:
        data, addr = sock.recvfrom(4096)

        msg = json.loads(data.decode("utf-8"))

        position = msg["position"]
        rotation = msg["rotation"]
        trigger = msg.get("trigger", 0.0)
        tracking_valid = msg.get(
            "tracking_valid", False
        )

        last_packet_time = time.monotonic()

        if not tracking_valid:
            print("Tracking invalid")
            continue

        print("From:", addr)
        print("Position:", position)
        print("Rotation:", rotation)
        print("Trigger:", trigger)

    except socket.timeout:
        if (last_packet_time is not None and
            time.monotonic() - last_packet_time > 0.5):
            print("Data timeout - stop control")

    except (ValueError, KeyError, TypeError) as e:
        print("Invalid packet:", e)
