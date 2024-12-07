from Data_Base0 import DataBase
from scrapy.crawler import CrawlerProcess
from chitaigorod import CGSpider
from Bookparser import DBPipeline
import Data_Base0 

db = DataBase()

process = CrawlerProcess()
DBPipeline.set_db(db)
CGSpider.set_pages_amount(1)
process.crawl(CGSpider)
process.start()