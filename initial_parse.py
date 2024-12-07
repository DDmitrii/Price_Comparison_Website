from Data_Base import DataBase
from scrapy.crawler import CrawlerProcess
from chitaigorod import CGSpider
from Bookparser import DBPipeline

db = DataBase("sqlite:///books.db")

process = CrawlerProcess()
CGSpider.set_pipeline(DBPipeline)
DBPipeline.set_db(db)
CGSpider.set_pages_amount(1) # Количество страниц Читай-города
process.crawl(CGSpider)
process.start()