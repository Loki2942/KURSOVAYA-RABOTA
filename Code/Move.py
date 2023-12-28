# Класс для каждого хода , при клике устанавливаются row_from и col_from ,
# при повторном клике устанавливаются  the row_to и col_to params
class Move:

    def __init__(self, row_from, col_from):
        self.row_from = row_from
        self.col_from = col_from
        self.row_to = -1
        self.col_to = -1
        self.have_dest = False

    # Функция возвращает значение row_from
    def get_row_from(self):
        return self.row_from

    # Функция возвращает значение the col_from
    def get_col_from(self):
        return self.col_from

    # Функция устанавливает значение row_from
    def set_row_from(self, row):
        self.row_from = row

    # Функция устанавливает значение col_from
    def set_col_from(self, col):
        self.col_from = col

    # Функция возвращает значение row_to
    def get_row_to(self):
        return self.row_to

    # Функция возвращает значение col_to
    def get_col_to(self):
        return self.col_to

    # Функция устанавливает row_to и  col_to
    def set_row_col_to(self, row_to, col_to):
        self.row_to = row_to
        self.col_to = col_to
        self.have_dest = True # меняем флаг


    # для отладки
    def __eq__(self, move):
        return self.row_from == move.row_from and self.col_from == move.col_from

    def __hash__(self):
        return hash((self.row_from, self.col_from))

    def __str__(self):

        return "Откуда({0}, {1}) ==> Куда({2}, {3})".format(self.row_from, self.col_from, self.row_to, self.col_to)
