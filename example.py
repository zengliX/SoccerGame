"""
An example using Soccer.py for simulation
"""

import Soccer
import numpy as np

np.random.seed(12)
env = Soccer.World()

ct = 1
while not env.game_done():
    print("Round {}".format(ct))
    action_a = env.random_action()
    action_b = env.random_action()
    print("A takes action: {}".format(action_a))
    print("B takes action: {}".format(action_b))

    env.take_both_actions('A', action_a, 'B', action_b)
    env.render_text()
    print("\n")

    ct += 1

