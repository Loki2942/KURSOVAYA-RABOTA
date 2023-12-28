from Move import Move
from Player import Player
import copy


class Ai(Player):

    def __init__(self, type, positions, board, turn):
        super().__init__(type, positions)
        self.board = board
        self.turn = turn
        self.pieces_columns = {None}
        self.init_pieces_columns(self.type, self.pieces_columns)

    def init_pieces_columns(self, color, pieces_columns):
        for i in range(2):
            for j in range(12):
                stack = self.board.board[i][j]
                try:
                    piece = stack.pick()
                    if piece.color != color:
                        continue
                    pieces_columns.add(piece)
                except IndexError:
                    continue
        try:
            pieces_columns.remove(None)
        except KeyError:
            print("Key Error")

    #  лучший ход для AI
    def play_ai_moves(self):
        played_moves = []
        path = []
        # если есть съеденные шашки
        if len(self.board.eaten_pieces.get("white")) > 0:
            cubes = self.turn.cubes
            current_cube_ind = 0
            entrances = self.board.can_piece_entrances_to_column(cubes[0].get_value(), cubes[1].get_value(), "white")
            while len(self.board.eaten_pieces.get("white")) > 0 and len(entrances) > 0:
                row = entrances[0].get("row")
                col = entrances[0].get("column")
                eat_piece = entrances[0].get("eat_piece")

                if col != -1:
                    self.turn.set_destination(Move(row, col), eat_piece, False)
                    self.board.return_eaten_piece_to_game("white", self.turn.destination)
                    self.turn.set_cube_played(current_cube_ind, True)
                    played_moves.append([Move(row, col), eat_piece, True])

                current_cube_ind = current_cube_ind + 1
                print(entrances.pop(0))

            self.turn.remove_destination()

        # Если не все шашки дома и нет съеденных
        if not (self.turn.has_all_cubes_playes()) and len(self.board.eaten_pieces.get("white")) == 0:
            path = self.get_all_paths(played_moves)
            if path:
                for cell in path:
                    move = cell[0]
                    eat_piece = cell[1]
                    if move.col_to == -1:
                        continue
                    if move.col_to > 11:
                        self.board.out_piece(move, "white")
                        continue
                    stack_source = self.board.board[move.row_from][move.col_from]
                    stack_dest = self.board.board[move.row_to][move.col_to]
                    if eat_piece:
                        try:
                            self.board.eat_piece(stack_dest.pick())
                        except IndexError:
                            print("Не важно")
                    print(move)

                    # self.board.make_move(move)
                    # self.board.change_piece_coordinates(move.row_from, move.col_from, move.row_to, move.col_to)
        return path

    # Это основная функция для  the AI_player
    # Эта функция проходиться по всем шашкам AI_player и для каждой проверяет лучшую комбинацию ходов
    # И лучшее место назначения в соответствии с наилучшей комбинацией
    # функция возвращает координаты наилучшей строки и столбца, к которым AI может переместиться в соответствии со значениями кубиков
    def get_all_paths(self, moves):
        cubes = self.turn.cubes
        double = cubes[0].get_value() == cubes[1].get_value()
        paths = []
        played_moves = moves.copy()
        append = 0
        best_score = -1000
        best_path = None
        for piece in self.pieces_columns.copy():
            for i in range(len(cubes)):
                if not (cubes[i].get_played()): # если не разыгран ход
                    final_move = Move(piece.row, piece.col)
                    destination = self.board.get_destination(self.type, final_move, cubes[i].get_value())
                    final_move.set_row_col_to(destination.row_from, destination.col_from)

                    source_legal, eat_piece = self.board.is_source_legal(self.type, final_move, self.all_home)

                    if source_legal: # если ходить можно
                        self.make_virtual_move(destination.row_from, destination.col_from, piece)
                        moves.clear()

                        if len(played_moves) > 0:
                            moves = played_moves.copy()

                        moves.append([final_move, eat_piece])
                        if not(cubes[abs((2-i)-1)].get_played()):
                            self.get_all_paths_for_first_move(len(cubes) - len(moves), cubes[abs((2-i)-1)].get_value(), moves, paths, double)
                        else:
                            paths.append(moves.copy())
                        self.undo_move(destination.row_from, destination.col_from, piece)

        return self.get_best_path(paths)

    def get_best_path(self, paths):
        best_score = -1000
        best_path = []
        for path in paths:
            path_score = self.evaluate(path)
            if path_score > best_score:
                best_score = path_score
                best_path = path.copy()
        return best_path

    # Эта функция возвращает все возможные ходы после первого хода
    # Получает:
    # cubes_number: число кубиков, если дубль - 3, если нет - 1
    # steps: количество ходов
    # moves: на каждой итерации этот массив хранит все возможные ходы,
    # и в конце мы добавляем этот массив в массив path
    # path: все возможные ходы
    # double: если кубики одинаковые, вернет True, если нет - False
    def get_all_paths_for_first_move(self, cubes_number, steps, moves, all_paths, double):
        if cubes_number == 0:
            return

        else:
            for piece in self.pieces_columns.copy():
                final_move = Move(piece.row, piece.col)
                destination = self.board.get_destination(self.type, final_move, steps)
                final_move.set_row_col_to(destination.row_from, destination.col_from)

                source_legal, eat_piece = self.board.is_source_legal(self.type, final_move, self.all_home)

                if source_legal:
                    self.make_virtual_move(destination.row_from, destination.col_from, piece)
                    moves.append([copy.deepcopy(final_move), eat_piece])
                    self.get_all_paths_for_first_move(cubes_number - 1, steps, moves, all_paths, double)
                    if len(moves) == 2 and not double or len(moves) == 4 and double:
                        all_paths.append(copy.deepcopy(moves))
                    self.undo_move(destination.row_from, destination.col_from, piece)
                    moves.pop(len(moves) - 1)

    # Эта функция делает виртуальный ход
    # Она получает строку и столбец назначения, а также шашку, которая сделает ход
    # И установливает текущую строку и столбец шашки на строку и столбец, переданные функции
    def make_virtual_move(self, dest_row, dest_col, piece):
        stack = self.board.board[piece.row][piece.col]
        try:
            piece = stack.pop()  # убираем шашку с доски
            temp = copy.deepcopy(piece)  # копия шашки

            if stack.stack_len() == 0:  # если стек пустой
                self.pieces_columns.discard(piece)  # удалить этуу шашку из массива pieces_columns

            temp.set_row(dest_row)
            temp.set_col(dest_col)

            self.board.board[dest_row][dest_col].push(temp)
            self.pieces_columns.add(temp)
        except IndexError:
            if dest_col > 11:
                self.board.out_pieces.get("white").append(piece)
            else:
                print("ПУСТАЯ ЯЧЕЙКА")

    # Эта функция отменяет ход
    # Функция получает исходную строку, исходный столбец и шашку
    # И возвращает шашку в исходную строку и исходный столбец
    # + функция возвращает шашку обратно в исходную строку и исходный столбец на доске
    def undo_move(self, dest_row, dest_col, piece):
        piece_row = piece.row
        piece_col = piece.col
        try:
            stack = self.board.board[dest_row][dest_col]
            try:
                temp = copy.deepcopy(stack.pick())
                if stack.stack_len() == 0:
                    self.pieces_columns.discard(temp)
            except IndexError:
                print("ПУСТАЯ ЯЧЕЙКА")
            # отмена хода
            move = Move(dest_row, dest_col)
            move.set_row_col_to(piece.row, piece.col)
            self.board.make_move(move)
            self.pieces_columns.add(piece)
        except IndexError:
            if dest_col > 11:
                self.board.board[piece.row][piece.col].push(piece)
                self.pieces_columns.add(piece)
            else:
                print("ПУСТАЯ ЯЧЕЙКА")

    # Эта функция оценивает ходы ]
    def evaluate(self, path):
        score = 0

        for tmp in path:
            move = tmp[0]
            s_row, s_col = move.row_from, move.col_from
            d_row, d_col = move.row_to, move.col_to

            stack_source = self.board.board[s_row][s_col]
            try:
                stack_dest = self.board.board[d_row][d_col]
            except IndexError:
                if d_col > 11:
                    if stack_source.stack_len() > 2:
                        score = score + 3000

                print("ВЫБРОС")

            eat_piece = tmp[1]
            if eat_piece:
                score = score + 150

            try:
                if stack_source.stack_len() == 2:
                    score = score - 100
                else:
                    score = score + 50
            except IndexError:
                score = score + 50

            if d_col > 11:
                score = score + 200
                continue

            if stack_dest.stack_len() >= 1:
                score = score + 50
            else:
                score = score - 100

        return score
