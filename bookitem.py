import scrapy

class BookItem(scrapy.Item):
    name = scrapy.Field()
    discountedprice = scrapy.Field()
    fullprice = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()
    websitename = scrapy.Field()