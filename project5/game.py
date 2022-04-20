import os
import typing as T
from exceptions import GameRuleException, NewGameException


class Game:
    ROWS = 6
    COLUMNS = 7
    SECTION_DIVIDER = '*' * 20

    WIN_SEQ_FOR_FIRST_PLAYER = 'x' * 4  # it is not calculated every time (little performance :-) )
    WIN_SEQ_FOR_SECOND_PLAYER = 'o' * 4

    def __init__(self):
        self.occupied_cells: T.Dict[int, list] = {
            column: [' ' for _ in range(self.ROWS)]
            for column in range(self.COLUMNS)
        }

        self.is_first_player_step: bool = True
        self.last_inserted_pos = tuple()
        self.last_error = ''

    def step(self):
        column: int = self.get_column_input()
        column -= 1  # it's easier for calculations

        if not (0 <= column < self.COLUMNS):
            self.last_error = 'Columns must be in 0 <= column < COLUMNS.'
            raise GameRuleException

        if ' ' not in self.occupied_cells[column]:
            self.last_error = 'Column is fulled.'
            raise GameRuleException

        occupied_column: T.List[str] = self.occupied_cells[column]
        for row in range(len(occupied_column) - 1, -1, -1):
            if occupied_column[row] == ' ':
                occupied_column[row] = 'x' if self.is_first_player_step else 'o'
                self.last_inserted_pos = (column, row)
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

    def is_end_game(self) -> T.Optional[bool]:
        win_sequence: str = self.WIN_SEQ_FOR_FIRST_PLAYER if self.is_first_player_step else self.WIN_SEQ_FOR_SECOND_PLAYER

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

        # check diagonals
        column, row = self.last_inserted_pos
        curr_player_sym = 'x' if self.is_first_player_step else 'o'

        sym_counts = 1  # current symbol is in suit
        curr_column = column - 1
        curr_row = row - 1

        # move left and up
        while curr_column >= 0 and curr_row >= 0:
            # if symbol does not belong player
            if curr_player_sym != self.occupied_cells[curr_column][curr_row]:
                break

            sym_counts += 1
            curr_column -= 1
            curr_row -= 1

        curr_column = column + 1
        curr_row = row + 1

        # move right and down
        while curr_column < self.COLUMNS and curr_row < self.ROWS:
            if curr_player_sym != self.occupied_cells[curr_column][curr_row]:
                break

            sym_counts += 1
            curr_column += 1
            curr_row += 1

        if sym_counts >= 4:
            return True

        # reset it - because it must count symbols by another diagonal
        sym_counts = 1
        curr_column = column + 1
        curr_row = row - 1

        # move right and up
        while curr_column < self.COLUMNS and curr_row >= 0:
            if curr_player_sym != self.occupied_cells[curr_column][curr_row]:
                break

            sym_counts += 1
            curr_column += 1
            curr_row -= 1

        curr_column = column - 1
        curr_row = row + 1

        # move left and down
        while curr_column >= 0 and curr_row < self.ROWS:
            if curr_player_sym != self.occupied_cells[curr_column][curr_row]:
                break

            sym_counts += 1
            curr_column -= 1
            curr_row += 1

        if sym_counts >= 4:
            return True

    def get_column_input(self) -> int:
        try:
            user_input: str = input(f'Enter column(1-{self.COLUMNS}),"n" - new game, "q" - for exit: ')

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
