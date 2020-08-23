import queue


class Store:
    def __init__(self):
        self.__store__ = queue.Queue()

    def push(self, data: tuple):
        self.__store__.put(data)

    def reset(self):
        self.__store__.clear()

    def pop(self):
        return self.__store__.get()

    @property
    def is_empty(self) -> bool:
        return self.__store__.empty()

    @property
    def store(self) -> queue.Queue:
        return self.__store__
