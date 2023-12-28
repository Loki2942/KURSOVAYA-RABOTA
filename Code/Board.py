import copy
from Stack import Stack
from Move import Move

PIECE_WIDTH, PIECE_HEIGHT = 75, 69
SPACE_BETWEEN_PIECES = 46
COLUMN_OVERFLOW_MULTIPLY = 20
ROW1_BOTTOM = 481
EATEN_AREA_WIDTH = 50
PADDING_BOARD_BORDERS = 25


# Класс доска
class Board:
    def __init__(self, red_player, white_player):
        self.red_player = red_player
        self.white_player = white_player
        self.board = [[], []]
        self.init_board()
        self.set_columns(self.red_player.pieces)
        self.set_columns(self.white_player.pieces)
        self.organize_pieces = [0, 0, 5, 10, 15, 15, 15, 15, 15, 15, 15, 15] # Эта часть параметров предназначена для уменьшения пикселей в столбцах слева направо
        self.eaten_pieces = {"red": [], "white": []}
        self.out_pieces = {"red": [], "white": []}

   # инициализируеv доску путем вставки в каждую ячейку  экземпляр Stack
    def init_board(self):
        for i in range(2):
            for j in range(12):
                self.board[i].append(Stack())

    # функция устанавливает вовсе столбцы доски стеки
    def set_columns(self, pieces_places):
        for i in range(len(pieces_places)):
            self.insert_piece(pieces_places[i])

    # устанавливаем новую шашку на место где она должна быть
    def insert_piece(self, piece):
        row = piece.row
        col = piece.col
        self.board[row][col].push(piece)

    def change_piece_coordinates(self, row_s, col_s, row_d, col_d):
        piece = self.board[row_s][col_s].pop()
        piece.set_row(row_d)
        piece.set_col(col_d)

        self.board[row_d][col_d].push(piece)

    #  определяем цвет игрока и возвращает его данные
    def get_player_details(self, color):
        if color == "red":
            return self.red_player
        return self.white_player

    # Эта функция проверяет, является ли выбранная позиция верной
    # 2 значения возвращает :
    # 1) Если позиция верная , возвращает True
    # 2) Если игрок сделает ход из этой позиции и съест фигуру противника вернет  true
    def is_source_legal(self, color, move, all_pieces_in_home):
        row_source = move.get_row_from()
        col_source = move.get_col_from()

        row_dest = move.get_row_to()
        col_dest = move.get_col_to()
        try:
            stack_source = self.board[row_source][col_source]
            if col_dest > 11:  # Если столбец назначения отсутствует на доске
                if not all_pieces_in_home:
                    return False, False
                elif stack_source.pick().get_color() == color:
                    return True, False
                else:
                    return False, False

            if stack_source.pick().get_color() != color:  #Если цвет шашки не совпадает с цвеом  текущего хода
                return False, False
        except IndexError as e:
            return False, False

        try:
            dest = self.board[row_dest][col_dest]
            if dest.pick().get_color() != color:  # Если цвет шашки, который находится в ячейке, не равен текущему цвету
                if dest.stack_len() == 1:  # Если в ячейке 1 шашка, значит ее можно сьесть
                    return True, True
                return False, False
        except IndexError as e:
            return True, False

        return True, False

    # проверяем правильно ли игрок выбрал ячейку и досткпна ли она 
    def is_destination_legal(self, clicked_coordinates, source_dest):
        row_click = clicked_coordinates.get_row_from()
        col_click = clicked_coordinates.get_col_from()

        row_dest = source_dest.get_row_to()
        col_dest = source_dest.get_col_to()

        if row_click == row_dest and col_click == col_dest:
            return True

        return False

    #  функция получает цвет шашки, начальную позицию и количество ходов, которые она должна выполнить
    def get_destination(self, color, start, steps):
        row_start = start.get_row_from()
        col_start = start.get_col_from()
        direction = 1

        if color == "red":
            direction = -1

        if row_start == 0 and color == "white" or row_start == 1 and color == "red":
            steps = steps * (-1)

        diff = col_start + steps

        if diff < 0:
            row_start += direction
            diff = abs(diff) - 1

        return Move(row_start, diff)

    # Эта функция выполняет перемещение от начальной позиции к назначенной
    def make_move(self, move):
        row_source = move.get_row_from()
        col_source = move.get_col_from()

        row_dest = move.get_row_to()
        col_dest = move.get_col_to()

        stack_dest_len = self.board[row_dest][col_dest].stack_len()

        move_piece = copy.deepcopy(self.board[row_source][col_source].pop())
        move_piece.set_row(row_dest)
        move_piece.set_col(col_dest)

        self.change_row_col_visual(move_piece, stack_dest_len, row_dest, col_dest)
        self.insert_piece(move_piece)

    def change_row_col_visual(self, move_piece, stack_dest_len, row_dest, col_dest):
        row_mul = SPACE_BETWEEN_PIECES

        if 4 - stack_dest_len < 0:
            stack_dest_len = abs(4 - stack_dest_len)
            row_mul = COLUMN_OVERFLOW_MULTIPLY

        if row_dest == 0:
            row_dest = (row_dest + stack_dest_len * row_mul) + 10
        else:
            row_dest = (ROW1_BOTTOM - stack_dest_len * row_mul)

        if col_dest < 6:
            col_dest = col_dest * PIECE_WIDTH + PADDING_BOARD_BORDERS - self.organize_pieces[col_dest]
        else:
            col_dest = col_dest * PIECE_WIDTH + PADDING_BOARD_BORDERS - self.organize_pieces[col_dest] + EATEN_AREA_WIDTH

        move_piece.set_row_visual(col_dest)
        move_piece.set_col_visual(row_dest)

    # Эта функция съедает тот шашку, которую ей передали
    # Для этого функция вызывает функцию, которая хранится в классе Player
    # она добавляет шашку в массив съеденных шашек
    # и в то же время удаляет ее из массива доступных шашек
    def eat_piece(self, piece):
        row = piece.get_row()
        col = piece.get_col()
        eaten_pieces = self.eaten_pieces.get("red")
        player = self.red_player

        temp = self.board[row][col].pop()
        if piece.get_color() == "white":
            eaten_pieces = self.eaten_pieces.get("white")
            player = self.white_player

        temp.set_col_visual(100 + (len(eaten_pieces) * PIECE_HEIGHT))
        temp.set_row_visual(453)
        temp.set_row(-1)
        temp.set_col(-1)
        eaten_pieces.append(temp)

    # Эта функция проверяет, может ли съеденная шашка попасть в один из  столбцов, которые сгенерировали кубики
    def can_piece_entrances_to_column(self, cube1_value, cube2_value, eaten_piece_color):
        available_entrances = []
        enemy_home_row = 0  # RED --> 0, WHITE --> 1

        if eaten_piece_color == "red":
            enemy_home_row = 1

        available_entrances.append(self.piece_entrance_options(eaten_piece_color,
                                                            {"row": enemy_home_row, "column": (11 - cube1_value) + 1}))
        available_entrances.append(self.piece_entrance_options(eaten_piece_color,
                                                            {"row": enemy_home_row,"column": (11 - cube2_value) + 1}))

        return available_entrances

    # Эта функция возвращает параметры входа --> {
    # column: столбец входа (-1 если вход недоступен)
    # eat_piece: если есть шашка, которая была съедена, когда эта шашка попала в этот столбец
    # }
    def piece_entrance_options(self, eaten_piece_color, coordinates):
        entrance_details = {"row": -1, "column": -1, "eat_piece": False}

        row = coordinates.get("row")
        col = coordinates.get("column")

        column = self.board[row][col]
        column_len = column.stack_len()

        if column_len == 0:  # Если в этом столбце нет шашки
            entrance_details["column"] = col

        elif column_len > 1:  # Если в этом столбце больше одной шашки
            if column.pick().color == eaten_piece_color:
                entrance_details["column"] = col

        elif column_len == 1:  # Если в этом столбце есть только одна шашка
            entrance_details["column"] = col
            if column.pick().color != eaten_piece_color:  # Если цвет шашки не совпадает с цветом съеденной шашки
                entrance_details["eat_piece"] = True

        entrance_details["row"] = row

        return entrance_details


    def can_enter(self, entrance_options):
        for entrance in entrance_options:
            row = entrance.get("row")
            col = entrance.get

    # возвращает съеденную шашку обратно в игру
    def return_eaten_piece_to_game(self, color, entrance):
        eaten_pieces = self.eaten_pieces.get("red")
        player = self.red_player
        organize = 46
        row, col = entrance.get("destination").get_row_from(), entrance.get("destination").get_col_from()
        can_eat_piece = entrance.get("eat_piece")
        temp_move = Move(row, col)
        temp_move.set_row_col_to(row, col)

        if color == "white":
            eaten_pieces = self.eaten_pieces.get("white")
            player = self.white_player
            organize = -46

        piece = eaten_pieces.pop(0)
        piece.set_row(row)
        piece.set_col(col)

        if can_eat_piece:
            self.eat_piece(self.board[row][col].pick())

        self.insert_piece(piece)
        player.add_piece(piece)

        self.make_move(temp_move)
        piece = self.board[row][col].pick()
        piece.set_col_visual(piece.col_visual + organize)

    # Эта функция вызывает функцию "are_all_pieces_in_home" в классе player,
    # в соответствии с цветом игрока, который получила функция.
    # Эта функция проверяет, все ли шашки игрока находятся в его доме
    # Эта функция возвращает результат "are_all_pieces_in_home", который в классе Player
    def are_all_pieces_in_home_for_player(self, color):
        player = self.white_player
        row_home = 1
        if color == "red":
            player = self.red_player
            row_home = 0

        if player.all_home:
            return True

        counter = self.number_of_pieces_in_home(row_home, color)

        if counter + len(self.out_pieces.get(color)) == 15:
            player.set_all_home(True)
            return True

        player.set_all_home(False)
        return False

    # Эта функция возвращает количество шашек в доме
    def number_of_pieces_in_home(self, row_home, color):
        counter = 0
        for i in range(6, 12):
            stack = self.board[row_home][i]

            try:
                if stack.pick().color == color:
                    counter += stack.stack_len()
            except IndexError:
                continue

        return counter

    # Эта функция выполняется для всех столбцов, в которых есть шашки с цветом, полученным функцией
    # и для каждого столбца функция проверяет, моожноли переместить шашку
    # Если шашка может переместиться на один из кубиков, она выходит из циклов и возвращает значение true
    # Если все шашки заблокированы, функция вернет значение false
    def check_if_blocked(self, cubes, color, all_pieces_in_home):
        blocked = True

        for i in range(2):
            for j in range(12):
                stack = self.board[i][j]
                try:
                    if stack.pick().color != color:
                        continue
                    final_move = Move(i, j)
                    for cube in cubes:
                        if not self.check_if_cube_blocked(color, final_move, cube, all_pieces_in_home):
                            blocked = False

                except IndexError:
                    continue

                if not blocked:
                    break

            else:
                continue

            break

        return blocked

    # Эта функция проверяет, может ли игрок сходить по значению кубика
    def check_if_cube_blocked(self, color, final_move, cube, all_pieces_in_home):
        temp_destination = self.get_destination(color, final_move, cube.get_value())
        final_move.set_row_col_to(temp_destination.get_row_from(), temp_destination.get_col_from())
        is_legal, eat_piece = self.is_source_legal(color, final_move, all_pieces_in_home)
        if not is_legal:
            return True

        return False

    # Эту функцию нужно вызывать, когда все шашки игрока находятся у него дома, и теперь ему нужно их выбросить
    def out_piece(self, piece_coordinates, color):
        row = piece_coordinates.get_row_from()
        col = piece_coordinates.get_col_from()
        piece = self.board[row][col].pop()
        self.out_pieces.get(color).append(piece)

    # Эта функция проверяет есть ли победитель
    def is_there_winner(self):
        counter_pieces_white = self.count_pieces("white")
        counter_pieces_red = self.count_pieces("red")
        winner = ""

        if counter_pieces_white == 0:
            winner = "white"

        if counter_pieces_red == 0:
            winner = "red"

        return winner != "", winner

    # Эта функция подсчитывает количество шашек для игрока с цветом "color"
    def count_pieces(self, color):
        counter = 0
        for i in range(2):
            for j in range(12):
                try:
                    stack = self.board[i][j]
                    if stack.pick().get_color() == color:
                        counter = counter + stack.stack_len()
                except IndexError:
                    continue

        return counter


    def set_player(self, color, new_player):
        player = self.red_player

        if type == "white":
            player = self.white_player

        player = new_player

    #
    def __str__(self):
        stacks = []
        for i in range(2):
            for j in range(12):
                stacks.append(self.board[i][j].__str__())
        return ", ".join(stacks)
