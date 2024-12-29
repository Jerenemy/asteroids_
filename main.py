from pygame import init, time
from engine.game_state import GameState
from utils import FPS, cleanup

def main():
    init()
    clock = time.Clock()
    game_state = GameState()
    while game_state.state != "exit":
        game_state.handle_events()
        # difference between update_game and render_game?
        # update_game calls update_objects, render_game calls render_objects.
        # so far, render_objects is where the 
        # where is the move method called? IN UPDATE_GAME.
        # update_game calls move method for all objects present 
        game_state.update_game()
        game_state.handle_collisions()
        game_state.render_game()
        clock.tick(FPS)
    cleanup()

if __name__ == "__main__":
    main()
