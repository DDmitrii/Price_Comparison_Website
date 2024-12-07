import requests
from bs4 import BeautifulSoup
class LivelibBook:
    name = ''
    tags = [
        """
        /list[str]
        """
    ]
    image = ''
    author = ''
    liveliblink = ''
    rating = ''
    price = 0
    def __init__(self, name, author, image, tags, liveliblink, rating):
        self.name = name
        self.author = author
        self.image = image
        self.tags = tags
        self.liveliblink = liveliblink
        self.rating = rating

def getLivelib(query):
    selector = '.aggbook-listview-biglist .object-edition'
    baselink = 'https://livelib.ru/find/books/'
    try:
        response = requests.get(baselink + query.replace(" ", "+"), timeout = 1) 
    except requests.exceptions.Timeout:
        print("Timeout")
        return None
    soup = BeautifulSoup(response.text, 'lxml')
    selected = soup.select(selector)
    if len(selected) == 0:
        return None
    item = selected[0]
    name = item.select('.brow-title .title')[0].text
    author = item.select('.object-info .description')[0].text
    image = item.select('.ll-redirect .object-cover')[0]['style'][15:-12]
    tags = [i.text for i in item.select_one('.object-info').select('.label-genre')]
    liveliblink = item.select('.ll-redirect a')[0]['href']
    rating = item.select('.stars-color-orange')[0].text
    return LivelibBook(name, author,image, tags, liveliblink, rating)