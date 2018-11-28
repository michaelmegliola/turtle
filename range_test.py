import VL53L1X
import time

lidar = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
lidar.open()
lidar.start_ranging(3)
while True:
    distance_in_mm = lidar.get_distance()
    print(distance_in_mm)
    time.sleep(.5)
lidar.stop_ranging()
