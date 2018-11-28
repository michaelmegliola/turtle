import time
import numpy as np
import rcpy
import rcpy.mpu9250 as mpu9250
from stepper import Stepper
import rcpy.motor as motor
from distancesensor import *

class BaseTurtle:

  #actions = ((1,1),(1,-1),(-1,1),(-1,-1))
  actions = ((1,1),(-1,-1),(0,0))
  
  def start(self):
    pass

  def get_state(self):
    return np.argmin(self.get_observation()[...,1])

  def exploit(self, q, heading=0):
    print('======================================')
    print(q)
    self.reset(heading)
    state = -1
    while state != 0:
      state = self.get_state()
      action = np.argmax(q[state])
      self.move(BaseTurtle.actions[action])
  
class ReplTurtle(BaseTurtle):

  def __init__(self, turn_degrees = 45):
    self.turn_degrees = turn_degrees
    self.reset(0)

  def move(self, action):
    if action[0] == 1:
      self.heading += self.turn_degrees
    elif action[0] == -1:
      self.heading -= self.turn_degrees
    self.heading = self.heading%360

  def reset(self, this_way = None):
    if this_way is None:
      self.heading = self.turn_degrees * np.random.randint(360//self.turn_degrees)
    else:
      self.heading = this_way
    return self.heading // 45

  def get_observation(self):
    readings = []
    for n in range(0, 360, 45):
      sensor_heading = (n - self.heading)%360
      if sensor_heading == 0:
        distance = 1.0
      elif sensor_heading == 45 or sensor_heading == 315:
        distance = 2**.5
      else:
        distance = 4.0
      readings.append([n,distance])
    return np.array(readings)

class Shelly(BaseTurtle):

    def start(self):
        rcpy.set_state(rcpy.RUNNING)

    def reset(self):
        return 0

    def move(self, action_vector):
        motor.motor1.set(action_vector[0] * 0.35)
        motor.motor2.set(action_vector[1] * 0.36)
        time.sleep(0.21)
        motor.motor1.set(action_vector[0] * 0.00)
        motor.motor2.set(action_vector[1] * 0.00)
    
    def stop(self):
        rcpy.exit()

class Ostritch(Shelly):

    def __init__(self):
        self.prev_nearfield_count = 0
        self.prev_nearfield_avg_distance = 0
        self.lidar = LidarSensor(8, 45)
    
    def reset(self, this_way = None):
        return None 
    
    def get_observation(self):
        return self.lidar.get_observation()

class TurtleEnv:

    def __init__(self, turtle, turn = 45, distance = 10):
        self.turtle = turtle
        self.turtle.start()

    def action_space(self):
        return self.actions

    def reset(self, this_way=None):
        self.count = 0
        return self.turtle.reset(this_way)

    def sample(self):
        return np.random.randint(len(BaseTurtle.actions))

    def step(self, action):
        self.turtle.move(BaseTurtle.actions[action])
        state = self.turtle.get_state()
        reward = 1 if state == 0 else -1
        return state, reward, reward > 0 

    def learn(self):
        explore = 0.1
        alpha = 0.1
        gamma = 0.9
        count = 0
        self.q = np.zeros((8, len(BaseTurtle.actions)))
        for n in range(1000):
            state = self.reset()
            done = False
            while not done:
                if np.random.random() < explore:
                    action = self.sample()
                else:
                    action = np.argmax(self.q[state])
                obs, reward, done = self.step(action)
                self.q[state][action] = (1-alpha) * self.q[state][action] + alpha * (reward + gamma * np.max(self.q[obs]))
                state = obs
                count += 1
            
        print(self.q)

    def solve(self, heading):
      print('\nsolving: ', heading)
      done = False
      state = self.reset(heading)
      while not done:
        action = np.argmax(self.q[state])
        obs, reward, done = self.step(action)
        print(self.turtle.heading, state, action, obs, reward, done)
        state = obs


#e = TurtleEnv(ReplTurtle())
e = TurtleEnv(Ostritch())
e.learn()

f = Ostritch()
f.exploit(e.q)


  
