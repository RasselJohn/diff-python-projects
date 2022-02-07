from exceptions import GameRuleException, NewGameException
from game import Game

g = Game()

while True:
    g.render()

    try:
        g.step()
    except GameRuleException:
        continue
    except NewGameException:
        g = Game()
        continue

    g.render()

    if g.is_end_game():
        print(f'Win {1 if g.is_first_player_step else 2} player!')
        break

    g.change_player()

input("Press any key for exit...")
