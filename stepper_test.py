import rcpy
import rcpy.clock as clock
import rcpy.motor as motor
import time

rcpy.set_state(rcpy.RUNNING)

states = [ (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0) ]
#states = [ (1, -1), (-1, -1), (-1, 1), (1, 1)]

direction = 1
direction_count = 0
step_interval = .003
reverse_count = 800
try:
    t0 = time.time() + step_interval
    count = 0
    while True:
        if (time.time() >= t0):
            motor.motor1.set(states[count][0])
            motor.motor2.set(states[count][1])
            count += direction
            if count == len(states):
                count = 0
            if count == -1:
                count = len(states) -1
            t0 = time.time() + step_interval
            direction_count +=1
            if direction_count >= reverse_count:
                direction = -direction
                direction_count = 0
finally:
    rcpy.exit()