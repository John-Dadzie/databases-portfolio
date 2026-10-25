"""Create two days of deterministic machine-shop readings as a CSV file."""

import csv
import math
import random
from datetime import datetime, timedelta
from pathlib import Path


def main():
    random.seed(42)
    machines = ["cnc-01", "cnc-02", "cnc-03"]
    start = datetime(2026, 1, 5, 6, 0, 0)
    days = 2
    step_seconds = 3
    points = days * 24 * 60 * 60 // step_seconds
    output = Path(__file__).with_name("telemetry.csv")

    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ts", "machine", "temp_c", "vib_rms", "spindle_load"])
        for index in range(points):
            timestamp = (start + timedelta(seconds=index * step_seconds)).isoformat(sep=" ")
            for machine in machines:
                temperature = 42 + 3 * math.sin(index / 500.0) + random.gauss(0, 0.6)
                vibration = 1.2 + 0.4 * math.sin(index / 90.0) + random.gauss(0, 0.08)
                load = 60 + 15 * math.sin(index / 300.0) + random.gauss(0, 3)
                if machine == "cnc-02":
                    vibration += 0.9 * (index / points)  # gradual bearing wear
                if random.random() < 0.0008:
                    vibration += random.uniform(0.4, 0.9)  # rare tool-chatter spike
                writer.writerow(
                    [timestamp, machine, f"{temperature:.2f}", f"{vibration:.3f}", f"{load:.1f}"]
                )

    print("Wrote {} ({} bytes; {} readings).".format(output, output.stat().st_size, points * len(machines)))


if __name__ == "__main__":
    main()
