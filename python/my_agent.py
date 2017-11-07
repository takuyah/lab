# Copyright 2016 Google Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""Basic random agent for DeepMind Lab."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import random
import numpy as np

import deepmind_lab


def _action(*entries):
  return np.array(entries, dtype=np.intc)


class MyAgent(object):
  """Simple agent for DeepMind Lab."""

  def __init__(self, action_spec):
    self.action_spec = action_spec
    print('Starting MyAgent. Action spec:', action_spec)

  ACTIONS = {
      'look_left': _action(-20, 0, 0, 0, 0, 0, 0),
      'look_right': _action(20, 0, 0, 0, 0, 0, 0),
      'look_up': _action(0, 10, 0, 0, 0, 0, 0),
      'look_down': _action(0, -10, 0, 0, 0, 0, 0),
      'strafe_left': _action(0, 0, -1, 0, 0, 0, 0),
      'strafe_right': _action(0, 0, 1, 0, 0, 0, 0),
      'forward': _action(0, 0, 0, 1, 0, 0, 0),
      'backward': _action(0, 0, 0, -1, 0, 0, 0),
      'fire': _action(0, 0, 0, 0, 1, 0, 0),
      'jump': _action(0, 0, 0, 0, 0, 1, 0),
      'crouch': _action(0, 0, 0, 0, 0, 0, 1)
  }

  # ACTION_LIST = ACTIONS.values()

  def step(self, unused_reward, unused_image):
    """Gets an image state and a reward, returns an action."""
    return MyAgent.ACTIONS['forward']

def run(length, width, height, fps, level):
  """Spins up an environment and runs the random agent."""
  env = deepmind_lab.Lab(
      level, ['RGB_INTERLACED'],
      config={
          'fps': str(fps),
          'width': str(width),
          'height': str(height)
      })

  env.reset()

  # Starts the random spring agent. As a simpler alternative, we could also
  # use DiscretizedRandomAgent().
  agent = MyAgent(env.action_spec())

  reward = 0

  for _ in xrange(length):
    if not env.is_running():
      print('Environment stopped early')
      env.reset()
      # agent.reset()
    obs = env.observations()
    action = agent.step(reward, obs['RGB_INTERLACED'])
    reward = env.step(action, num_steps=1)

  print('Finished after %i steps. Total reward received is %f'
        % (length, agent.rewards))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--length', type=int, default=1000,
                      help='Number of steps to run the agent')
  parser.add_argument('--width', type=int, default=80,
                      help='Horizontal size of the observations')
  parser.add_argument('--height', type=int, default=80,
                      help='Vertical size of the observations')
  parser.add_argument('--fps', type=int, default=60,
                      help='Number of frames per second')
  parser.add_argument('--runfiles_path', type=str, default=None,
                      help='Set the runfiles path to find DeepMind Lab data')
  parser.add_argument('--level_script', type=str, default='nav_maze_random_goal_03',
                      help='The environment level script to load')

  args = parser.parse_args()
  if args.runfiles_path:
    deepmind_lab.set_runfiles_path(args.runfiles_path)
  run(args.length, args.width, args.height, args.fps, args.level_script)
