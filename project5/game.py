import os

from exceptions import GameRuleException, NewGameException


class Game:
    ROWS = 6
    COLUMNS = 7
    SECTION_DIVIDER = '*' * 20

    WIN_SEQ_FOR_FIRST_PLAYER = 'x' * 4  # it is not calculated every time (little performance :-) )
    WIN_SEQ_FOR_SECOND_PLAYER = 'o' * 4

    def __init__(self):
        self.occupied_cells = {
            column: [' ' for _ in range(self.ROWS)]
            for column in range(self.COLUMNS)
        }
        self.is_first_player_step = True
        self.last_error = ''

    def step(self):
        column = self.get_column_input()
        column -= 1  # it's easier for calculations

        if not (0 <= column < self.COLUMNS):
            self.last_error = 'Columns must be in 0 <= column < COLUMNS.'
            raise GameRuleException

        if ' ' not in self.occupied_cells[column]:
            self.last_error = 'Column is fulled.'
            raise GameRuleException

        occupied_column = self.occupied_cells[column]
        for i in range(len(occupied_column) - 1, -1, -1):
            if occupied_column[i] == ' ':
                if self.is_first_player_step:
                    occupied_column[i] = 'x'
                else:
                    occupied_column[i] = 'o'

                break

    def render(self):
        os.system('cls||clear')
        print("\bConnect 4 v1.0")

        print(self.SECTION_DIVIDER)

        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                print('|', end='')
                print(self.occupied_cells[column][row], end='')

            print('|')

        print(self.SECTION_DIVIDER)

        print(f'Step of {1 if self.is_first_player_step else 2} player.')

        if self.last_error:
            print(self.last_error)
            self.last_error = ''

    def is_end_game(self):
        win_sequence = self.WIN_SEQ_FOR_FIRST_PLAYER if self.is_first_player_step else self.WIN_SEQ_FOR_SECOND_PLAYER

        # check win sequence
        for i in self.occupied_cells.values():
            joined_cells = ''.join(i)
            if win_sequence in joined_cells:
                return True

        # transpose and check win sequence
        for i in map(list, zip(*self.occupied_cells.values())):
            joined_cells = ''.join(i)
            if win_sequence in joined_cells:
                return True

    def get_column_input(self):
        try:
            user_input = input(f'Enter column(1-{self.COLUMNS}),"n" - new game, "q" - for exit: ')

            if user_input == 'n':
                raise NewGameException
            elif user_input == 'q':
                exit(0)

            return int(user_input)
        except ValueError:
            self.last_error = f'Must be integer number  between 1 and {self.COLUMNS}'
            raise GameRuleException

    def change_player(self):
        self.is_first_player_step = not self.is_first_player_step
