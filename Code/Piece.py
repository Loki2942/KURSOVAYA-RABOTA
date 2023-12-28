# Класс для одной шашки (красную или белую)
class Piece:
    def __init__(self, color, image, row, col, row_visual, col_visual):
        self.color = color
        self.image = image
        self.row = row
        self.col = col
        self.row_visual = row_visual
        self.col_visual = col_visual

    # Функция возвращает цвет шашки
    def get_color(self):
        return self.color

    #Функция возвращает картинку шашки
    def get_img(self):
        return self.image

    # Функция возвращает текущую строку
    def get_row(self):
        return self.row

    # Функция устанавливает строку из полученной
    def set_row(self, row):
        self.row = row

    # Функция возвращает текущий столбец шашки
    def get_col(self):
        return self.col

    # Функция устанавливает столбец
    def set_col(self, col):
        self.col = col

    # Функция возвращает строку для ототбражения на доске
    def get_row_visual(self):
        return self.row_visual

    #  Функция устанавливает строку для ототбражения на доске
    def set_row_visual(self, row_visual):
        self.row_visual = row_visual

    # Функция возвращает столбец для ототбражения на доске
    def get_col_visual(self):
        return self.col_visual

    #  Функция устанавливает столбец для ототбражения на доске
    def set_col_visual(self, col_visual):
        self.col_visual = col_visual

    #  True если шашки имеют одно и ту же строку и столбец, False если нет
    def __eq__(self, piece):
        return self.row == piece.row and self.col == piece.col

    def __hash__(self):
        return hash((self.row, self.col))

    # все данные о шашке
    def __str__(self):
        return "Color = {0}\nImage = {1}\nRow = {2}\nColumn = {3}\n".format(self.color, self.image, self.row, self.col)
