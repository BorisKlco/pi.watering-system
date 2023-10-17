import time

last_watering = time.time()

while True:
    time.sleep(1) # 1 hour - 3600
    watering_diff = time.time() - last_watering
    dry_soil = False # sensor_output()
    print(watering_diff)
