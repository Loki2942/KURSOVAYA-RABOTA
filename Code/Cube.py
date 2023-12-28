# Класс для одного кубика
class Cube():

    def __init__(self, value):
        self.value = value  # Значения кубика (1-6)
        self.played = False  # True если кубик разыгран False если нет

    # Функция возвращает текущее значение кубика
    def get_value(self):
        return self.value

    # Функция устанавливает новое значение кубика
    def set_value(self, value):
        self.value = value

    # Функция возвращает текущее значение параметра played
    def get_played(self):
        return self.played

    # Функция устанавливает новое значение параметра played
    # Если игрок не сходил -  True
    # Если сходил - False
    def set_played(self, played):
        self.played = played

    def __str__(self): # для отладки
        return "Значение: {0}".format(self.value)



