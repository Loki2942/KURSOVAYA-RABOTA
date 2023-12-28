# Класс  для поля (стек)  список в котором все данные о шашках на текущей ячейке
class Stack:

    def __init__(self):
        self.stack = []

    #  Функция возвращает верхний элемент
    def pick(self):
        return self.stack[0]

    #  Функция возвращает верхний элемент и удаляет его
    def pop(self):
        return self.stack.pop(0)

    # Функция вставляет шашку в конец(наверх) верхний элемент
    def push(self, value):
        self.stack.insert(0, value)

    # отладка в строку
    def __str__(self):
        return "\n".join(str(val) for val in self.stack)

    # все элементы стека
    def get_all_stack_elements(self):
        temp_s = Stack()
        values = []

        for i in range(len(self.stack)):
            values.append(self.pick())
            temp_s.push(self.pop())

        for i in range(len(temp_s.stack)):
            self.push((temp_s.pop()))

        return values

    # Функция возвращает длину стека
    def stack_len(self):
        return len(self.stack)
