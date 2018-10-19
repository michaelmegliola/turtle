import rcpy
import rcpy.clock as clock
import rcpy.motor as motor
import time


class Stepper:
    states = [ (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0) ]
    #states = [ (1, -1), (-1, -1), (-1, 1), (1, 1)]

    def __init__(self, stepper_index = 1):
        if stepper_index == 1:
            self.output1 = motor.motor1
            self.output2 = motor.motor2
        if stepper_index == 2:
            self.output1 = motor.motor3
            self.output2 = motor.motor4

    def start(self):
        rcpy.set_state(rcpy.RUNNING)

    def stop(self):
        rcpy.exit()

    def reset(self):
        pass


    def move(self, direction):
        step_interval = .003
        step_count = abs(direction) * 100
        t0 = time.time() + step_interval
        loop_count = 0
        step = 0
        while loop_count < step_count:
            if (time.time() >= t0):
                self.output1.set(self.states[count][0])
                self.output2.set(selfstates[count][1])
                step += direction
                if step == len(self.states):
                    step = 0
                if step == -1:
                    step = len(self.states) -1
                t0 = time.time() + step_interval
                loop_count += 1
