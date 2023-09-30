# PGCROW
Pgcrow is a pygame framework for making simple games.

## Installation
**_With pip_**
```
pip install git+https://github.com/KentAugust/pgcrow.git
```

**_With poetry_**
```
poetry add git+https://github.com/KentAugust/pgcrow.git
```

## Overview
**_Workflow_**
```
- First create a window with the setting you want.
- Next create a game.
- Then add scene with scene manager and change to that scene.
    - You can also overwrite scene manage with a new instance and set a initial scene.   
- Finally run the game.
```

**_Running the game_**


```
Using Game.run:
- init window screen
- start initial scene
- set window title

After that the game loop start.

Game loop execution order:
    - get deltatime
    - clean the window
    - loop events
        - mouse and keybord handle their own events
    - update scene manager
        - update current scene
        - update current scene transition if it's active
    - render scene manager
        - render current scene
        - render current scene transition if it's active
    - get update function
        - if you are using display variant window, here it's where is scaled
    - render screen scene manager
        - render current scene directly onto screen
    - update display
        - update display with pygame.display.update (except for Gl windows
          variants, use pygame.display.flip manually)
    - clock tick
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

## Contributions:
Feel free to make pull requests, changes suggestions and comments.
