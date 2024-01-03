import random
import numpy as np



class Connect4:
    def __init__(self):
        self.moves = 42 * [0]
        self.winners = (0, 0)
        self.tree_depth = 3

    def reset(self):
        self.moves = 42 * [0]
        self.winners = (0, 0)

    def get_winners(self):
        return self.winners

    def is_valid_move(self, col):
        if col == -1:
            return False

        is_valid_move = False
        for i in range(41 - (6 - col), -1, -7):
            if self.moves[i] == 0:
                is_valid_move = True
                break
        return is_valid_move

    def game_over(self, player_turn, grid=None):
        if self.horizontal_win(player_turn, False, grid) or self.vertical_win(player_turn, False, grid):
            return "Win"
        if self.right_diagonal_win(player_turn, False, grid) or self.left_diagonal_win(player_turn, False, grid):
            return "Win"
        if self.draw():
            return "Draw"
        return "Continue"

    def draw(self):
        for m in self.moves:
            if m == 0:
                return False
        return True

    def horizontal_win(self, player_turn, heuristic, grid=None):
        count = 0
        m = 1 if player_turn else 2
        if grid is None:
            rows = [self.moves[i:i + 7] for i in range(0, 41, 7)]
        else:
            rows = [grid[i:i + 7] for i in range(0, 41, 7)]
        for i in range(len(rows)):
            for j in range(4):
                if rows[i][j] == rows[i][j + 1] == rows[i][j + 2] == rows[i][j + 3] == m:
                    if heuristic:
                        count += 1
                    else:
                        self.winners = (7 * i + j, 7 * i + j + 3)
                        return True
        return count if heuristic else False

    def vertical_win(self, player_turn, heuristic, grid=None):
        count = 0
        m = 1 if player_turn else 2
        if grid is None:
            cols = [[self.moves[i + j] for i in range(0, 41, 7)] for j in range(7)]
        else:
            cols = [[grid[i + j] for i in range(0, 41, 7)] for j in range(7)]
        for i in range(len(cols)):
            for j in range(3):
                if cols[i][j] == cols[i][j + 1] == cols[i][j + 2] == cols[i][j + 3] == m:
                    if heuristic:
                        count += 1
                    else:
                        self.winners = (i + 7 * j, i + 7 * (j + 3))
                        return True
        return count if heuristic else False

    def right_diagonal_win(self, player_turn, heuristic, grid=None):
        m = 1 if player_turn else 2
        right_diagonals = []
        self.set_seq(right_diagonals, 4, 3, 20, True, grid)
        self.set_seq(right_diagonals, 5, 4, 13, True, grid)
        self.set_seq(right_diagonals, 6, 5, 6, True, grid)
        return self.diag_contains_win(right_diagonals, m, heuristic)

    def left_diagonal_win(self, player_turn, heuristic, grid=None):
        m = 1 if player_turn else 2
        left_diagonals = []
        self.set_seq(left_diagonals, 4, 3, 14, False, grid)
        self.set_seq(left_diagonals, 5, 2, 7, False, grid)
        self.set_seq(left_diagonals, 6, 1, 0, False, grid)
        return self.diag_contains_win(left_diagonals, m, heuristic)

    def set_seq(self, diagonals, r, f, b, right_diag, grid=None):
        dist = 6 if right_diag else 8
        seq1 = []
        seq2 = []
        if grid is None:
            grid_to_evaluate = self.moves
        else:
            grid_to_evaluate = grid
        for i in range(r):
            seq1.append((f + dist * i, grid_to_evaluate[f + dist * i]))
            seq2.append((b + dist * i, grid_to_evaluate[b + dist * i]))
        diagonals.append(seq1)
        diagonals.append(seq2)

    def diag_contains_win(self, diagonals, m, heuristic):
        count = 0
        for diag in diagonals:
            if len(diag) == 4:
                if diag[0][1] == diag[1][1] == diag[2][1] == diag[3][1] == m:
                    if heuristic:
                        count += 1
                    else:
                        self.winners = (diag[0][0], diag[3][0])
                        return True
            if len(diag) == 5:
                for i in range(2):
                    if diag[i][1] == diag[i + 1][1] == diag[i + 2][1] == diag[i + 3][1] == m:
                        if heuristic:
                            count += 1
                        else:
                            self.winners = (diag[i][0], diag[i + 3][0])
                            return True
            if len(diag) == 6:
                for i in range(3):
                    if diag[i][1] == diag[i + 1][1] == diag[i + 2][1] == diag[i + 3][1] == m:
                        if heuristic:
                            count += 1
                        else:
                            self.winners = (diag[i][0], diag[i + 3][0])
                            return True

        return count if heuristic else False

    def find_height(self, col, y_pixel_centers):
        for i in range(41 - (6 - col), -1, -7):
            if self.moves[i] == 0:
                m = 5 if 35 <= i <= 41 else 4 if 28 <= i <= 34 else 3 if 21 <= i <= 33 else 2 if 14 <= i <= 20 else 1 if 7 <= i <= 13 else 0
                return y_pixel_centers[m]

    def get_moves(self):
        return self.moves

    def get_rows(self):
        return [self.moves[i:i + 7] for i in range(0, 41, 7)]

    def get_columns(self):
        return [[self.moves[i + j] for i in range(0, 41, 7)] for j in range(7)]

    def set_a_move(self, player_turn, col):
        for i in range(41 - (6 - col), -1, -7):
            if self.moves[i] == 0:
                self.moves[i] = 1 if player_turn else 2
                break

    def get_valid_moves(self, grid=None):
        valid_moves = []
        if grid is None:
            columns = self.get_columns()
        else:
            columns = [[grid[i + j] for i in range(0, 41, 7)] for j in range(7)]
        for i in range(7):
            for j in range(5, -1, -1):
                if columns[i][j] == 0:
                    valid_moves.append((i, 7 * j + i))
                    break
        return valid_moves

    def play_computer_move(self, i):
        self.moves[i] = 2

    def random_agent(self):
        return random.choice(self.get_valid_moves())

    def play_diagonals(self, player_turn, r, heuristic=False, grid=None):
        count = 0
        valid_moves = [i[1] for i in self.get_valid_moves()]
        diagonals = []
        self.set_seq(diagonals, 4, 3, 20, True, grid)
        self.set_seq(diagonals, 5, 4, 13, True, grid)
        self.set_seq(diagonals, 6, 5, 6, True, grid)
        self.set_seq(diagonals, 4, 3, 14, False, grid)
        self.set_seq(diagonals, 5, 2, 7, False, grid)
        self.set_seq(diagonals, 6, 1, 0, False, grid)
        for diag in diagonals:
            if len(diag) == 4:
                temp_diag = [diag[0], diag[1], diag[2], diag[3]]
                values = [i[1] for i in temp_diag]
                if values.count(player_turn) == r:
                    if heuristic:
                        count += 1
                    else:
                        for t_d in temp_diag:
                            if t_d[1] == 0 and t_d[0] in valid_moves:
                                return t_d[0] % 7, t_d[0]
            if len(diag) == 5:
                for i in range(2):
                    temp_diag = [diag[i], diag[i + 1], diag[i + 2], diag[i + 3]]
                    values = [i[1] for i in temp_diag]
                    if values.count(player_turn) == r:
                        if heuristic:
                            count += 1
                        else:
                            for t_d in temp_diag:
                                if t_d[1] == 0 and t_d[0] in valid_moves:
                                    return t_d[0] % 7, t_d[0]
            if len(diag) == 6:
                for i in range(3):
                    temp_diag = [diag[i], diag[i + 1], diag[i + 2], diag[i + 3]]
                    values = [i[1] for i in temp_diag]
                    if values.count(player_turn) == r:
                        if heuristic:
                            count += 1
                        else:
                            for t_d in temp_diag:
                                if t_d[1] == 0 and t_d[0] in valid_moves:
                                    return t_d[0] % 7, t_d[0]
        return count if heuristic else -1

    def play_horizontal(self, player_turn, r, heuristic=False, grid=None):
        count = 0
        valid_moves = [i[1] for i in self.get_valid_moves()]
        if grid is None:
            rows = [self.moves[i:i + 7] for i in range(0, 41, 7)]
        else:
            rows = [grid[i:i + 7] for i in range(0, 41, 7)]
        rows_values = []
        for i in range(len(rows)):
            temp_row = []
            for j in range(7):
                temp_row.append((j + 7 * i, rows[i][j]))
            rows_values.append(temp_row)

        for row in rows_values:
            for i in range(4):
                temp_row = [row[i], row[i + 1], row[i + 2], row[i + 3]]
                values = [k[1] for k in temp_row]
                if values.count(player_turn) == r:
                    if heuristic:
                        count += 1
                    else:
                        for t_p in temp_row:
                            if t_p[1] == 0 and t_p[0] in valid_moves:
                                return t_p[0] % 7, t_p[0]
        return count if heuristic else -1

    def play_vertical(self, player_turn, r, heuristic=False, grid=None):
        count = 0
        valid_moves = [i[1] for i in self.get_valid_moves()]
        if grid is None:
            cols = [[self.moves[i + j] for i in range(0, 41, 7)] for j in range(7)]
        else:
            cols = [[grid[i + j] for i in range(0, 41, 7)] for j in range(7)]
        for i in range(len(cols)):
            for j in range(3):
                temp_col = [(i + 7 * j, cols[i][j]), (i + 7 * (j + 1), cols[i][j + 1]),
                            (i + 7 * (j + 2), cols[i][j + 2]), (i + 7 * (j + 3), cols[i][j + 3])]
                values = [k[1] for k in temp_col]
                if values.count(player_turn) == r:
                    if heuristic:
                        count += 1
                    else:
                        for t_c in temp_col:
                            if t_c[1] == 0 and t_c[0] in valid_moves:
                                return i, t_c[0]
        return count if heuristic else -1

    def default_agent(self):
        if self.play_diagonals(2, 3) != -1:
            return self.play_diagonals(2, 3)
        elif self.play_horizontal(2, 3) != -1:
            return self.play_horizontal(2, 3)
        elif self.play_vertical(2, 3) != -1:
            return self.play_vertical(2, 3)
        elif self.play_diagonals(1, 3) != -1:
            return self.play_diagonals(1, 3)
        elif self.play_horizontal(1, 3) != -1:
            return self.play_horizontal(1, 3)
        elif self.play_vertical(1, 3) != -1:
            return self.play_vertical(1, 3)
        elif self.play_diagonals(2, 2) != -1:
            return self.play_diagonals(2, 2)
        elif self.play_horizontal(2, 2) != -1:
            return self.play_horizontal(2, 2)
        elif self.play_vertical(2, 2) != -1:
            return self.play_vertical(2, 2)
        else:
            return self.random_agent()

    def drop_piece(self, grid, col, mark):
        next_grid = grid.copy()
        for row in range(6 - 1, -1, -1):
            if next_grid[row][col] == 0:
                break
        next_grid[row][col] = mark
        return next_grid

    def check_window(self, window, num_discs, piece):
        return (window.count(piece) == num_discs and window.count(0) == 4 - num_discs)

    def count_windows(self, grid, num_discs, piece):
        num_windows = 0
        for row in range(6):
            for col in range(4):
                window = list(grid[row, col:col + 4])
                if self.check_window(window, num_discs, piece):
                    num_windows += 1
        for row in range(3):
            for col in range(7):
                window = list(grid[row:row + 4, col])
                if self.check_window(window, num_discs, piece):
                    num_windows += 1
        for row in range(3):
            for col in range(4):
                window = list(grid[range(row, row + 4), range(col, col + 4)])
                if self.check_window(window, num_discs, piece):
                    num_windows += 1
        for row in range(3, 6):
            for col in range(4):
                window = list(grid[range(row, row - 4, -1), range(col, col + 4)])
                if self.check_window(window, num_discs, piece):
                    num_windows += 1
        return num_windows

    def get_heuristic(self, grid, mark):
        num_threes = self.count_windows(grid, 3, mark)
        num_fours = self.count_windows(grid, 4, mark)
        num_threes_opp = self.count_windows(grid, 3, mark % 2 + 1)
        num_fours_opp = self.count_windows(grid, 4, mark % 2 + 1)
        score = num_threes - 1e2 * num_threes_opp - 1e4 * num_fours_opp + 1e6 * num_fours
        return score

    def score_move(self, grid, col, mark, nsteps, alpha, beta):
        next_grid = self.drop_piece(grid, col, mark)
        score = self.minimax(next_grid, nsteps - 1, False, mark, alpha, beta)
        return score

    def is_terminal_window(self, window):
        return window.count(1) == 4 or window.count(2) == 4

    def is_terminal_node(self, grid):
        # Check for draw
        if list(grid[0, :]).count(0) == 0:
            return True
        # Check for win: horizontal, vertical, or diagonal
        # horizontal
        rows = 6
        inarow = 4
        columns = 7
        for row in range(rows):
            for col in range(4):
                window = list(grid[row, col:col + inarow])
                if self.is_terminal_window(window):
                    return True
        # vertical
        for row in range(3):
            for col in range(columns):
                window = list(grid[row:row + inarow, col])
                if self.is_terminal_window(window):
                    return True
        # positive diagonal
        for row in range(3):
            for col in range(4):
                window = list(grid[range(row, row + inarow), range(col, col + inarow)])
                if self.is_terminal_window(window):
                    return True
        # negative diagonal
        for row in range(3, rows):
            for col in range(4):
                window = list(grid[range(row, row - inarow, -1), range(col, col + inarow)])
                if self.is_terminal_window(window):
                    return True
        return False

    def minimax(self, node, depth, maximizingPlayer, mark, alpha, beta):
        is_terminal = self.is_terminal_node(node)
        valid_moves = [c for c in range(7) if node[0][c] == 0]
        if depth == 0 or is_terminal:
            return self.get_heuristic(node, mark)

        if maximizingPlayer:
            value = -np.Inf
            for col in valid_moves:
                child = self.drop_piece(node, col, mark)
                value = max(value, self.minimax(child, depth - 1, False, mark, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cut-off
            return value
        else:
            value = np.Inf
            for col in valid_moves:
                child = self.drop_piece(node, col, mark % 2 + 1)
                value = min(value, self.minimax(child, depth - 1, True, mark, alpha, beta))
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha cut-off
            return value

    def minimax_agent(self, mark, tree_depth):
        self.tree_depth = tree_depth
        valid_moves = [i[0] for i in self.get_valid_moves()]
        grid = np.asarray(self.moves).reshape(6, 7)
        alpha = -np.Inf
        beta = np.Inf
        scores = dict(
            zip(valid_moves, [self.score_move(grid, col, mark, self.tree_depth, alpha, beta) for col in valid_moves]))
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        chosen_col = random.choice(max_cols)
        for move in self.get_valid_moves():
            if move[0] == chosen_col:
                return move
