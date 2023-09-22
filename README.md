# PGCROW
Pgcrow is a pygame framework for making simple games.

## Installation
```
pip install git+https://github.com/KentAugust/pycrow.git
```

## Overview
**_Workflow_**
- First create a window with the setting you want.
- Next create a game.
- Then add scene with scene manager and change to that scene.
    - You can also overwrite scene manage with a new instance and set a initial scene.   
- Finally run the game.

**_Running the game_**

This is how game loop looks like.
```
1 - Gets deltatime
2 - Clean the window
3 - Loop events
    3.1 - All inputs handles events
4 - Scene manager update current scene
    4.1 - Update scene
    4.2 - Update transition if not finished
5 - Scene manager render current scene
    5.1 - Render scene
    5.2 - Render transition if not finished
6 - Update/flip the window
7 - Set clock ticks
```

## Examples
There are two ways to run the examples:

Directly with python:
```
python -m pgcrow.examples.example_name
```
In a python file:
```python
# import the example class
from pgcrow.examples.example_name import example_class

example_class().run()
```

See all [examples](examples).
## Notes:
- WindowScreenGl can't change window size for the moment.

## Contributions:
Feel free to make pull requests, changes suggestions and comments.
