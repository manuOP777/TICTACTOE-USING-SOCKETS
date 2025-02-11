# tic_tac_toe.py
class TicTacToe:
    def __init__(self, player_symbol):
        self.symbol_list = [" "] * 9  # Initializes a 3x3 grid
        self.player_symbol = player_symbol

    def restart(self):
        self.symbol_list = [" "] * 9  # Clears the grid

    def draw_grid(self):
        print("\n       A   B   C\n")
        for i in range(3):
            row = f"   {i + 1}   " + " ║ ".join(self.symbol_list[i * 3:(i + 1) * 3])
            print(row)
            if i < 2:
                print("      ═══╬═══╬═══")
        print()

    def edit_square(self, grid_coord):
        if len(grid_coord) != 2 or grid_coord[0] not in '123' or grid_coord[1].upper() not in 'ABC':
            print("Invalid coordinate! Please enter in format (e.g., A1, B2, 3C).")
            return

        col = grid_coord[1].upper()
        row = grid_coord[0]

        grid_index = (int(row) - 1) * 3 + (ord(col) - ord('A'))

        if self.symbol_list[grid_index] == " ":
            self.symbol_list[grid_index] = self.player_symbol
        else:
            print("This square is already taken! Choose another.")

    def update_symbol_list(self, new_symbol_list):
        self.symbol_list = new_symbol_list.copy()

    def did_win(self, player_symbol):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6],              # Diagonals
        ]
        return any(all(self.symbol_list[i] == player_symbol for i in combo) for combo in winning_combinations)

    def is_draw(self):
        return not self.did_win(self.player_symbol) and " " not in self.symbol_list
