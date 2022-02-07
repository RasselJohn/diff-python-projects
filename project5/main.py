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

        is_new_game = input("New game(y/n)?")
        if is_new_game == 'y':
            g = Game()
            continue

        break

    g.change_player()
