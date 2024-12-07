from Data_Base0 import DataBase
from scrapy.crawler import CrawlerProcess
from chitaigorod import CGSpider
from Bookparser import DBPipeline

db = DataBase()

process = CrawlerProcess()
CGSpider.set_pipeline(DBPipeline)
DBPipeline.set_db(db)
CGSpider.set_pages_amount(1)
process.crawl(CGSpider)
process.start()