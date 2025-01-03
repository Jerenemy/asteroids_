from pygame import init, time
from engine.game_state import GameState
from utils import FPS, cleanup

def main():
    init()
    clock = time.Clock()
    game_state = GameState(lives=1)
    while game_state.state != "exit":
        game_state.handle_events()
        game_state.update_game()
        game_state.handle_collisions()
        game_state.render_game()
        game_state.play_sounds()
        clock.tick(FPS)
    cleanup()

if __name__ == "__main__":
    main()