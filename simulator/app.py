import random
import time
from prometheus_client import Gauge, start_http_server

DEVICE_UP = Gauge("device_up", "Device reachability (1=up, 0=down)", ["device_id", "rack"])
CPU_USAGE = Gauge("device_cpu_usage_percent", "CPU utilization %", ["device_id", "rack"])
MEM_USAGE = Gauge("device_memory_usage_percent", "Memory utilization %", ["device_id", "rack"])
PING_MS = Gauge("device_ping_latency_ms", "Network ping latency in ms", ["device_id", "rack"])

DEVICES = [
    (f"device-{i:03d}", "rack-a" if i <= 10 else "rack-b")
    for i in range(1, 21)
]

if __name__ == "__main__":
    start_http_server(8000)
    start_time = time.time()
    print("Fleet telemetry exporter running on :8000/metrics")

    while True:
        elapsed = time.time() - start_time
        for device_id, rack in DEVICES:
            is_down = (device_id == "device-003" and 30 <= elapsed <= 240)

            if is_down:
                DEVICE_UP.labels(device_id=device_id, rack=rack).set(0)
                CPU_USAGE.labels(device_id=device_id, rack=rack).set(0)
                MEM_USAGE.labels(device_id=device_id, rack=rack).set(0)
                PING_MS.labels(device_id=device_id, rack=rack).set(0)
            else:
                DEVICE_UP.labels(device_id=device_id, rack=rack).set(1)
                CPU_USAGE.labels(device_id=device_id, rack=rack).set(round(random.uniform(12.0, 78.0), 1))
                MEM_USAGE.labels(device_id=device_id, rack=rack).set(round(random.uniform(25.0, 82.0), 1))
                PING_MS.labels(device_id=device_id, rack=rack).set(round(random.uniform(1.5, 18.0), 2))

        time.sleep(5)
