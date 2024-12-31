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

## Update 2: 28/12/24
Significantly improved overall structure, modularized, simplified, etc.

**graphics**: contains all graphics-related implementation, eg animations, hud, title, game_over

**entities**: improved ABC structure of each entity. Included a should_despawn method.

*asteroid.py*: added self.polygon attribute to init RandomPolygon object to modularize display

*spaceship.py*: also added polygon attribute. This will help with displaying lives in corner.


**utils**: utils are coming along swimmingly

*geometry.py*: Implemented shape classes for asteroid and spaceeship.

*pygame_helpers.py*: Implemented detecting one event when a key is pressed by instantiating an object for the key in question. 

## Steps
1. Asteroid destruction sequence (splitting) DONE
2. Spaceship destruction sequence
3. Finish updating spaceship.py 
4. Spaceship rocket
5. Spaceship invincibility
2. game_over screen and play again ability
3. Increasing difficulty
4. Pause functionality
5. Animations 
6. Sounds
9. Automated spaceships
10. Make asteroids look better
11. Add sigmoidal rotation function

## Next
Resolve bug of spaceship destroy animation: I believe it is due to passing reference (list) instead of copy (immutable tuple) 

Also need to have Spaceship not display during the duration of the spaceship destruction sequence. Could do this by editing Spaceship.destroy(), but that seems like a bad solution, since then have to keep track of both timers simultaneously and they need to be synced. Possible, but is there a better solution?

## Next
1. Base rotation off of spaceship speed, have them not all always rotate same direction.
2. Do spaceship rocket.
3. All other stuff
4. clean up display.py