import rcpy
import rcpy.clock as clock
import rcpy.motor as motor
import time


class Stepper:
    #states = [ (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0) ]
    #states = [ (1, -1), (-1, -1), (-1, 1), (1, 1)]
    states = [ (0.15, -0.15), (0.0, -0.15), (-0.15, -0.15), (-0.15, 0.15), (-0.15, 0.15), (0.0, 0.15), (0.15, 0.15), (0.15, 0.0) ]
    step_interval = 0.01
    degrees_per_step = 0.9
    
    def __init__(self, stepper_index = 1):
        self.position = 0
        self.n = 0
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

    def move(self, degrees):
        t0 = time.time() + Stepper.step_interval
        steps = int(round(degrees)/Stepper.degrees_per_step) # 0.9 degrees per step
        
        for x in range(abs(steps)):
            while (time.time() < t0):
                pass
            self.output1.set(Stepper.states[self.n][0])
            self.output2.set(Stepper.states[self.n][1])
            self.n += -1 if degrees > 0 else 1
            self.n %= len(Stepper.states)
            t0 = time.time() + Stepper.step_interval
        #self.output1.set(0)
        #self.output2.set(0)

        self.position += steps * Stepper.degrees_per_step