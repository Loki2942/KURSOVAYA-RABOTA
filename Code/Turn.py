import random, copy
from Cube import Cube


# Класс для единичного хода в игре
class Turn:

    def __init__(self, ai_game):
        self.red_turn = True
        self.color = "red"
        self.player_clicks = []
        self.cubes = []
        self.chosen_cube = 0
        self.generate_cubes()
        self.source = None
        self.destination = None
        self.double_ind = -1
        self.ai_game = ai_game
        if ai_game:
            self.red_turn = False
            self.color = "white"
            self.ai_turn = True

    # функция для смены  очереди хода
    def change_turn(self):
        if self.ai_game:
            if self.ai_turn:
                self.ai_turn = False
                self.color = "red"
                self.red_turn = True
            else:
                self.ai_turn = True
                self.color = "white"
                self.red_turn = False
        else:
            if self.red_turn:
                self.red_turn = False
                self.color = "white"
            else:
                self.red_turn = True
                self.color = "red"
        self.generate_cubes()

    # Эта функция генерирует 2 случайных числа  1-6 и вставляет их в массив cubes
    def generate_cubes(self):
        cube1 = Cube(random.randint(1, 6))
        cube2 = Cube(random.randint(1, 6))

        self.chosen_cube = 0

        if cube1.get_value() == cube2.get_value(): # если дубль
            self.cubes = [cube1, copy.deepcopy(cube1), copy.deepcopy(cube1), copy.deepcopy(cube1)]
            self.double_ind = 0
        else:
            self.cubes = [cube1, cube2]
            self.double_ind = -1

    #  функция изменяет номер выбранного кубика
    def set_chosen_cube(self, cube_number):
        self.chosen_cube = cube_number
        self.clear_clicks()

    # функция возвращает номер хода
    def get_number_of_steps(self):
        return self.cubes[self.chosen_cube].get_value()

    #  функция добавляет новый клик ко всем кликам игрока в этом ходу
    def add_click(self, click):
        self.player_clicks.append((click))

    #  функция очищает клики игрока
    def clear_clicks(self):
        self.player_clicks.clear()

    # функция устанавливает новый источник для этого хода
    def set_source(self, source):
        self.source = source

    # функция устанавливает пункт назначения, в который игроку необходимо передать выбранную фигуру.
    def set_destination(self, destination, eat_piece, out_own_piece):
        self.destination = {"destination": destination, "eat_piece": eat_piece, "out_own_piece": out_own_piece}

    # функция удаляет destination, устанавливая его значение равным None
    def remove_destination(self):
        self.destination = None

    def remove_source(self):
        self.source = None

    # Эта функция получает номер кубика и его статус
    # и устанавливает их для кубика, который имеет значение параметра cube_number
    def set_cube_played(self, cube_number, played):
        self.cubes[cube_number].set_played(played)
        self.chosen_cube = 3 - (2 + cube_number)

    #  функция возвращает значение True, если все кубики были сыграны, и значение False, если нет
    def has_all_cubes_playes(self):
        for i in range(len(self.cubes)):
            if not self.cubes[i].get_played():
                break
        else:
            return True

        return False

    # функция увеличивает двойной индекс и тем самым переходит к следующему партии из 4 кубиков
    def increase_double_index(self):
        self.double_ind = self.double_ind + 1

    def __str__(self):
        return "Red turn: {0}, player clicks: {1}, cubes: {2}, chosen cube: {3}".format(self.red_turn,
                                                                                        self.player_clicks,
                                                                                        self.cubes,
                                                                                        self.chosen_cube)
