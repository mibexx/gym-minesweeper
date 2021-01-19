# [GYM] Minesweeper Environment

A simple minesweeper environment for gym.


## Initialize
```python
import gym

env = gym.make('mibexx_gym_minesweeper:mibexx-gym-minesweeper-v0')
env.reset()
```


## Environment

### State
Observation space:  (9, 9)

```
[[0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]]
```

### Actions
Action space:  [9 9]

Action is a (y,x) tuple.

Example for row 3 col 2:
```python
state, reward, done, _ = env.step((3, 2))
```


## Rewards
empty field: 1  
already clicked field: -1   
a mine: -10  