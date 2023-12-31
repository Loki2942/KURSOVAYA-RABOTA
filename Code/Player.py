from Piece import Piece


# Класс для игрока
class Player:

    def __init__(self, type, positions):
        self.type = type
        self.pieces = []
        self.set_pieces(positions)
        self.eaten = []
        self.row_home = 0
        if type == "white":
            self.row_home = 1
        self.all_home = False

    # Функция возвращает все шашки игрока
    def get_pieces(self):
        return self.pieces

    # Функция устанавливает все шашки игрока в параметр pieces(это класс Piece)
    def set_pieces(self, positions):
        image = "white.png"
        if self.type == "red":
            image = "red.png"

        for i in range(15):
            x = int(positions[i][1]/263)
            y = int(positions[i][0]/75)
            self.pieces.append(Piece(self.type, image, x, y, positions[i][0], positions[i][1]))

    def add_piece(self, piece):
        self.pieces.append(piece)

    #  Функция упорядочивает шашки для начала игры
    def start_game(self):
        if self.type == "red":
            pass
        elif self.type == "white":
            pass

    # добавляет съеденную шашку в съеденный список
    def add_piece_eaten(self, piece):
        self.eaten.append(piece)

    # Функция для проверки все ли шашки дома(для вывода с доски)
    def set_all_home(self, all__home):
        self.all_home = all__home

    # все данные вывод
    def __str__(self):
        pieces = []
        for piece in self.pieces:
            pieces.append(piece.__str__())
            pieces.append("-------------------\n")

        return " ".join(pieces)