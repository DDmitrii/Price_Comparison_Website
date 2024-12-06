class Book:
    name = ''
    tags = [
        """
        /list[str]
        """
    ]
    image = ''
    author = ''
    liveliblink = ''
    price = 0
    def __init__(self, name, author, image, tags, liveliblink):
        self.name = name
        self.author
        self.image = image
        self.tags = tags
        self.liveliblink = liveliblink
        pass

class DataBase:
    def searchByTags(*args) -> list[Book]: # Поиск похожих книг по тегам
        pass
    def getBook(*args) -> list[Book]: # Поиск таргетно одной книжки на разных сайтах
        pass

class InputOutput:
    def getInput(*args):
        pass
    def output(*args):
        pass