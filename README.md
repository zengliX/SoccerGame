# Soccer Game environment

This repository can be used to simulate the **Soccer Game** environment as described in the following paper:

> Greenwald, A., Hall, K., & Serrano, R. (2003, August). Correlated Q-learning. In ICML (Vol. 3, pp. 242-249) 


### User manual

```python
#Create soccer world environment. The default grid size is (2, 4), as specified in the paper.
env = World()

# List all actions
env.actions

# Get a random action from all actions
env.random_action()

# Get player state
env.player_state(player)

# get states after both player take actions
# action will result in stick if it takes player out of the grid
env.take_both_actions(player1, action1, player2, action2)

# test if game is over
env.game_done()

# display game state
env.render_text()
```

### Example
The `example.py` file contains the following simulation example:

```python
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
    print()

    ct += 1
```

Game process is shown below (`*` represents the ball):

```bash
Round 1
A takes action: S
B takes action: S
A           B
-------------
|  |  |  |  |
-------------
|  |B*|A |  |
-------------


Round 2
A takes action: W
B takes action: N
A           B
-------------
|  |B*|  |  |
-------------
|  |  |A |  |
-------------


Round 3
A takes action: S
B takes action: S
A           B
-------------
|  |  |  |  |
-------------
|  |B*|A |  |
-------------


Round 4
A takes action: 0
B takes action: E
A           B
-------------
|  |  |  |  |
-------------
|  |B |A*|  |
-------------


Round 5
A takes action: W
B takes action: 0
A           B
-------------
|  |  |  |  |
-------------
|  |B*|A |  |
-------------


Round 6
A takes action: W
B takes action: N
A           B
-------------
|  |B*|  |  |
-------------
|  |  |A |  |
-------------


Round 7
A takes action: S
B takes action: N
A           B
-------------
|  |B*|  |  |
-------------
|  |  |A |  |
-------------


Round 8
A takes action: E
B takes action: E
A           B
-------------
|  |  |B*|  |
-------------
|  |  |  |A |
-------------


Round 9
A takes action: 0
B takes action: N
A           B
-------------
|  |  |B*|  |
-------------
|  |  |  |A |
-------------


Round 10
A takes action: W
B takes action: S
A           B
-------------
|  |  |B |  |
-------------
|  |  |A*|  |
-------------


Round 11
A takes action: 0
B takes action: S
A           B
-------------
|  |  |B |  |
-------------
|  |  |A*|  |
-------------


Round 12
A takes action: W
B takes action: E
A           B
-------------
|  |  |  |B |
-------------
|  |A*|  |  |
-------------


Round 13
A takes action: N
B takes action: N
A           B
-------------
|  |A*|  |B |
-------------
|  |  |  |  |
-------------


Round 14
A takes action: E
B takes action: 0
A           B
-------------
|  |  |A*|B |
-------------
|  |  |  |  |
-------------


Round 15
A takes action: S
B takes action: W
A           B
-------------
|  |  |B |  |
-------------
|  |  |A*|  |
-------------


Round 16
A takes action: E
B takes action: E
A           B
-------------
|  |  |  |B |
-------------
|  |  |  |A*|
-------------
```

