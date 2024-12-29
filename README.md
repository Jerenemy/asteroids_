## Steps

1. Create more general underlying classes
2. Create util.py file
3. Create bash cat script
4. Turn the button_down fix into a function


## Update 1: 18/12/24
Modularized code to have more subfolders:

**engine**: contains files that control underlying functionality of the game, eg state, high scores, level

**entities**: create entities that live in the game, eg asteroids, asteroid_list, bullet, spaceship, window

**utils**: contains standalone functions useful to other files for modularization

**data**: contains high_scores.json

**main.py**: main game loop

## Todo:
1. Remove tight coupling in all util files

2. Write game_state.py: needs to contain everything necessary for maintaining the game state, displaying things too?

3. use ABC for every single type of thing

