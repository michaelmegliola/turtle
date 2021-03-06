#import turtle
import time
import numpy as np
import rcpy
import rcpy.mpu9250 as mpu9250
from stepper import Stepper
import rcpy.motor as motor
from distancesensor import *

X = 0
Y = 1
Z = 2

class BaseTurtle:

    #actions = ((1,1),(1,-1),(-1,1),(-1,-1))
    actions = ((1,1),(-1,-1))

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

    def start(self):
        rcpy.set_state(rcpy.RUNNING)
        time.sleep(.5)
        mpu9250.initialize(enable_magnetometer = False)
        time.sleep(.5)

    def reset(self):
        self.xyz = [0,0,0]
        return 0

    def move(self, action_vector):
        
        t_0 = time.time()
        t_stop = t_0 + 0.21
        t_sensing = t_0 + 0.20  # was .25
        t1 = t_0
        
        max_accel = [0,0,0]
        min_accel = [0,0,0]
        
        max_gyro = [0,0,0]
        min_gyro = [0,0,0]
        motor.motor1.set(action_vector[0] * 0.35)
        motor.motor2.set(action_vector[1] * 0.36)
        count = 0
        while t1 <= t_stop:
            if t1 <= t_sensing:
                data = mpu9250.read()
                max_accel = np.maximum(max_accel, data['accel'])
                min_accel = np.minimum(min_accel, data['accel'])
                max_gyro = np.maximum(max_gyro, data['gyro'])
                min_gyro = np.minimum(min_gyro, data['gyro'])
                count += 1
            t1 = time.time()
        
        motor.motor1.set(action_vector[0] * 0.00)
        motor.motor2.set(action_vector[1] * 0.00)
        if max_gyro[Z] > 150.0:
            return 'TL'
        elif min_gyro[Z] < -150.0:
            return 'TR'
        elif max_accel[Y] > abs(min_accel[Y]):
            return 'F'
        else:
            return 'R'
    
    def stop(self):
        rcpy.exit()

class Ostritch(Shelly):

    def __init__(self):
        self.prev_nearfield_count = 0
        self.prev_nearfield_avg_distance = 0
        self.lidar = LidarSensor(9, 45)
        
    
    def get_observation(self):
        return self.lidar.get_observation()
        

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
        reward = 0
        nearfield_count = 0
        nearfield_total = 0
        minimum = 9999
        angle_min = -1
        self.turtle.move(BaseTurtle.actions[action])
        observations = self.turtle.get_observation()
        for obs in observations:
            print('Heading = {0:+.3f}'.format(obs[0]),'Distance = {0:+.1f}'.format(obs[1]))
        state = np.argmin(observations[...,1])
        closest_obs = observations[state]
        print('Best heading:', closest_obs)
        reward = pow(180 - abs(closest_obs[0]), 2)
        self.count += 1
        return state, reward, self.count > 12

    def learn(self):
        explore = 0.4
        alpha = 0.1
        gamma = 0.9
        q = np.zeros((9, len(BaseTurtle.actions)))
        for n in range(100):
            state = self.reset()
            done = False
            while not done:
                if np.random.random() < explore:
                    action = self.sample()
                else:
                    action = np.argmax(q[state])
                obs, reward, done = s.step(action)
                #q[obs][action] = (1-alpha) * q[state][action] + alpha * reward
                q[obs][action] = (1-alpha) * q[state][action] + alpha * (reward + gamma * np.max(q[obs]))
                state = obs
            explore *= 0.99
            print(q)
            print("Explore rate: ,", explore)
    


s = TurtleEnv(turtle = Ostritch(), turn = 45, distance = 10)
s.turtle.start()
time.sleep(1)
s.reset()
s.learn()
s.turtle.stop()

'''s = TurtleEnv(turtle = Ostritch(), turn = 45, distance = 10)
s.turtle.start()
time.sleep(1)
s.reset()
observation = s.turtle.get_observation()
for obs in observation:
    print('Heading = {0:+.3f}'.format(obs[0]),'Distance = {0:+.1f}'.format(obs[1]))
s.turtle.stop()'''