import rcpy
import rcpy.clock as clock
import rcpy.motor as motor
import time

rcpy.set_state(rcpy.RUNNING)

#states = [ (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0) ]
states = [ (1, -1), (-1, -1), (-1, 1), (1, 1)]

try:
    t0 = time.time() + 1
    count = 0
    while True:
        if (time.time() >= t0):
            motor.motor1.set(states[count][0])
            print('Switching motor state:', states[count][0], states[count][1])
            motor.motor2.set(states[count][1])
            count +=1
            if count == 4:
                count = 0
            t0 = time.time() + 1
finally:
    rcpy.exit()