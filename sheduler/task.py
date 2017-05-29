import os

class task:
    def __init__(self, name, data):
        self.__name = name
        self.__data = data
    
    def get_name(self):
        return self.__name

    def get_data(self):
        return self.__data

def new(name, data):
    return task(name, data)
