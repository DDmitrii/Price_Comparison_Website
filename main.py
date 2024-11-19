class Book:
    name = ''
    tags = [
        """
        /list[str]
        """
    ]
    price = 0
    def __init__(self):
        pass

class DataBase:
    def searchByTags(*args) -> list[Book]: # Поиск похожих книг по тегам
        pass
    def getBook(*args) -> list[Book]: # Поиск таргетно одной книжки на разных сайтах
        pass

class Parser:
    def searchBy(*args) -> list[Book]:
        pass

class InputOutput:
    def getInput(*args):
        pass
    def output(*args):
        pass