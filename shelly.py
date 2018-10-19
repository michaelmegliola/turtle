#import turtle
import time
import numpy as np
import rcpy
import rcpy.mpu9250 as mpu9250
from stepper import Stepper
import rcpy.motor as motor

class BaseTurtle:

    actions = ((1,1),(1,-1),(-1,1),(-1,-1))

    def __init__(self):
        self.xyz = [0,0,0]

    def get_xyz(self):
        return self.xyz

class VirtualTurtle(BaseTurtle):

    def start(self):
        pass

    def reset(self):
        turtle.pensize(6)
        turtle.clear()
        turtle.penup()
        turtle.goto(0,0)
        turtle.pendown()
        self.xyz = [0,0,0]
        return 0

    def move(self, action_vector):
        if action_vector[0] == action_vector[1]:
            turtle.forward(action_vector[0])
            self.xyz = (10, 0, 0)
        else:
            turtle.left(action_vector[0])
            self.xyz = (0, 0, action_vector[0]*45)

class Shelly(BaseTurtle):

    bipolar1 = Stepper()
    bipolar2 = Stepper(2)

    def start(self):
        rcpy.set_state(rcpy.RUNNING)
        time.sleep(.5)
        #mpu9250.initialize(enable_dmp = True, dmp_sample_rate = 100, enable_fusion = False, enable_magnetometer = True)
        mpu9250.initialize(enable_magnetometer = False)
        time.sleep(.5)

    def reset(self):
        self.xyz = [0,0,0]
        return 0

    def move(self, action_vector):
        t0 = time.time() + .5
        t1 = time.time() + .05
        max_xyz = [0, 0, 0]
        #motor.motor1.set(action_vector[0] * .25)
        #motor.motor2.set(action_vector[1] * .26)
        while time.time() <= t0:
            if time.time() > t1:
                max_xyz.append(mpu9250.read())
                t1 = time.time() + .05
            print('Reading array length: ',len(max_xyz))
        time.sleep(.25)
    
    def stop(self):
        rcpy.exit()


class TurtleEnv:

    def __init__(self, turtle = Shelly(), turn = 45, distance = 10):
        self.turtle = turtle
        self.turn_degrees = turn
        self.move_distance = distance
        self.turtle.start()

    def action_space(self):
        return self.actions

    def reset(self):
        self.count = 0
        return self.turtle.reset()

    def sample(self):
        return np.random.randint(len(BaseTurtle.actions))

    def step(self, action):
        action_vector = BaseTurtle.actions[action]
        print(action_vector)
        self.turtle.move(action_vector)
        xyz = self.turtle.get_xyz()
        reward = xyz[0] - abs(xyz[2])
        self.count += 1
        return action, reward, self.count > 100

    def learn(self):
        explore = 1.0
        alpha = 0.1
        gamma = 0.9
        q = np.zeros((len(BaseTurtle.actions),len(BaseTurtle.actions)))
        for n in range(100):
            state = self.reset()
            done = False
            while not done:
                if np.random.random() < explore:
                    action = self.sample()
                else:
                    action = np.argmax(q[state])
                obs, reward, done = s.step(action)
                q[state][action] = (1-alpha) * q[state][action] + alpha * reward
                state = obs
            explore *= 0.9
            print(q)
    


s = TurtleEnv()
s.turtle.start()
time.sleep(1)
s.reset()
#s.learn()

direction = 2
for x in range(10):
    s.step(direction)
    t0 = time.time() + 0.5
    for i in range(50):
        if time.time() > t0:
            #print('Y accel:', mpu9250.read()['accel'][1])
            t0 = time.time() + 0.1
    if direction == 2:
        direction = 0
    else:
        direction = 2
s.turtle.stop()
