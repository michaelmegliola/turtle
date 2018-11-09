from stepper import *
import VL53L1X

class DistanceSensor:
    
    def __init__(self, sweep_count = 3, sweep_degrees = 30):
        self.sweep_count = sweep_count
        self.sweep_degrees = sweep_degrees
        self.position = 0.0  # 0 is forward
        
    def get_reading(self, position):
        self.seek_position(position)
        return self.read_distance()
        
    def seek_position(self, position):
        pass
    
    def read_distance(self):
        pass
        
class LidarSensor(DistanceSensor):
    
    def __init__(self, sweep_count, sweep_degrees):
        super().__init__(sweep_count, sweep_degrees)
        self.lidar = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
        self.stepper = Stepper(2)
        
    def seek_position(self, position):
        current_lidar_pos = self.stepper.position
        self.stepper.move(position - self.position)
        self.position += self.stepper.position - current_lidar_pos
        
l = LidarSensor(3,30)
for x in range(6):
    l.seek_position(60)
    print(l.position, l.stepper.position)
    l.seek_position(-30)
    print(l.position, l.stepper.position)
l.seek_position(0)
print(l.position, l.stepper.position)