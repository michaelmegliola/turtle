#import turtle
import time
import numpy as np
import rcpy
import rcpy.mpu9250 as mpu9250
from stepper import Stepper

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

    def move(self, distance):
        turtle.forward(distance)
        self.xyz = (distance, 0, 0)

    def turn(self, degrees):
        turtle.left(degrees)
        self.xyz = (0, 0, degrees)

class Shelly(BaseTurtle):

    bipolar1 = Stepper()
    bipolar2 = Stepper()

    def start(self):
        rcpy.set_state(rcpy.RUNNING)
        time.sleep(.5)
        mpu9250.initialize(enable_dmp = True, dmp_sample_rate = 100, enable_fusion = True, enable_magnetometer = True)
        time.sleep(.5)

    def reset(self):
        self.xyz = [0,0,0]
        return 0

    def move(self, distance):
        self.bipolar1.move(distance)
        self.bipolar2.move(distance)
        self.xyz = (distance, 0, 0)

    def turn(self, degrees):
        self.bipolar1.move(degrees)
        self.bipolar2.move(-degrees)
        self.xyz = (0, 0, mpu9250.read()['tb'][2] * 57.29578)

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
        self.turtle.bipolar1.move(action_vector[0])
        self.turtle.bipolar2.move(action_vector[1])
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

s.reset()
s.learn()
s.turtle.done()
