import rcpy
import rcpy.clock as clock
import rcpy.motor as motor
import time


class Stepper:
    states = [ (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0) ]
    #states = [ (1, -1), (-1, -1), (-1, 1), (1, 1)]
    
    def __init__(self):
        pass
    
    def start(self):
        rcpy.set_state(rcpy.RUNNING)
    
    def stop(self):
        rcpy.exit()
    
    def reset(self):
        pass
    
    def sweep(self):
        direction = 1
        step_interval = .003
        reverse_count = 800
        t0 = time.time() + step_interval
        count = 0
        while True:
            if (time.time() >= t0):
                motor.motor1.set(self.states[count][0])
                motor.motor2.set(selfstates[count][1])
                motor.motor3.set(self.states[7-count][0])
                motor.motor4.set(self.states[7-count][1])
                count += direction
                if count == len(self.states):
                    count = 0
                if count == -1:
                    count = len(self.states) -1
                t0 = time.time() + step_interval
                direction_count +=1
                if direction_count >= reverse_count:
                    direction = -direction
                    direction_count = 0        

    
    def move(self, direction):
        step_interval = .003
        step_count = abs(direction) * 100
        t0 = time.time() + step_interval
        loop_count = 0
        step = 0
        while loop_count < step_count:
            if (time.time() >= t0):
                motor.motor1.set(self.states[step][0])
                motor.motor2.set(self.states[step][1])
                motor.motor3.set(self.states[7-step][0])
                motor.motor4.set(self.states[7-step][1])
                step += direction
                if step == len(self.states):
                    step = 0
                if step == -1:
                    step = len(self.states) -1
                t0 = time.time() + step_interval
                loop_count += 1


        