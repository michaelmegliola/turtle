from turtle import *
import time
import math
import numpy as np
#import rcpy

#PLATFORM = ROBOT     # Enable if running on a physical robot
PLATFORM = 'PYTHON'     # Enable if running as a python simulation

class Sheldon:

  def __init__(self):
    self.rotation = 0
    self.total_travel = 0
    if PLATFORM == 'ROBOT':
      rcpy.set_state(rcpy.RUNNING)
    else:
      color('red', 'yellow')
      begin_fill()

  def start(self):
    mpu9250.initialize(enable_dmp = True, dmp_sample_rate = 100, enable_fusion = True, enable_magnetometer = True)
    # Do other starty stuff

  def get_attitude(self):
    return np.multiply(mpu9250.read()['tb'], 57.29578)

  def turn_left(self):
    # code to control motors TBA
    if PLATFORM == 'PYTHON':
      left(45)
    self.rotation += 45
    if self.rotation > 360:
      self.rotation -= 360

  def turn_right(self):
    # code to control motors TBA
    if PLATFORM == 'PYTHON':
      right(45)
    self.rotation -= 45
    if self.rotation < 0:
      self.rotation = 360 - self.rotation

  def move_fwd(self):
    # code to control motors TBA
    if PLATFORM == 'PYTHON':
      forward(1)

  def move_back(self):
    # code to control motors TBA
    if PLATFORM == 'PYTHON':
      backward(1)

  def sample(self):
    return np.random.randint(3)

  def step(self, action):
    if action == 1:
      self.turn_left()
    if action == 2:
      self.turn_right()
    if action == 3:
      self.move_fwd()
    if action == 4:
      self.move_back()

    diff = 0.0
    if PLATFORM == 'ROBOT':
      t0 = time.time() + 0.085
      while time.time() < t0:  # assumes each loop takes apx same amount of time
        accel = mpu9250.read()['accel']
        diff += accel[0] - abs(accel[1])
      time.sleep(0.25)
    else:
      # funky circle math to compute dx/dy based on heading; assume heading 0 is along +X axis
      x = math.cos(math.radians(self.rotation))
      y = math.sin(math.radians(self.rotation))
      if action == 3:
        diff = x - abs(y)
      elif action == 4:
        diff = -x - abs(y)
    self.total_travel += diff
    done = bool(self.total_travel > 20)  # arbitrary value until we do some testing
    reward = diff
    return self.rotation, reward, done

  def learn(self):
    alpha = 0.10
    explore = 1.0
    q = np.zeros(4,4)
    for i in range (1000):
      state = 0
      self.step(state)
      done = False
      while not done:
        if np.random.random() < explore:
          action = self.sample()
        elif np.argmax(q[state]) > 0:
          action = np.argmax(q[state])
        else:
          action = self.sample()
        obs, reward, done = self.step(action)
        # This next section needs adjustment once we determine observation stuff
        '''
        q[state][obs] = alpha * q[state][obs] + (1 - alpha) * (reward + np.max(q[obs]))
        state = obs
        '''
        explore *= .9
        explore = max(explore, .01)

s = Sheldon()
