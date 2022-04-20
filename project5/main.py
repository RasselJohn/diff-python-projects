from exceptions import GameRuleException, NewGameException
from game import Game

game = Game()

while True:
    game.render()

    try:
        game.step()
    except GameRuleException:
        continue
    except NewGameException:
        game = Game()
        continue

    game.render()

    if game.is_end_game():
        print(f'Win {1 if game.is_first_player_step else 2} player!')

        is_new_game = input("New game(y/n)?")
        if is_new_game == 'y':
            game = Game()
            continue

        break

    game.change_player()
