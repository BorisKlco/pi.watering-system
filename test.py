import time
import math

last_watering = time.time()
SLEEP_INTERVAL = 1  # 1 hour - 3600
WATERING_INTERVAL = 6  # 12 hour - 43200

while True:
    time.sleep(SLEEP_INTERVAL)
    watering_diff = math.floor(time.time() - last_watering)
    water_now = True if watering_diff > WATERING_INTERVAL else False
    dry_soil = False  # sensor_output()
    print("INFO: ", last_watering, water_now)
    if dry_soil or water_now:
        print("WATERING!!!")
        last_watering = time.time()
