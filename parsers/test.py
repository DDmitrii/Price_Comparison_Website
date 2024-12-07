from scrapy.crawler import CrawlerProcess
from mif import MIFSpider
from chitaigorod import CGSpider
from labirint import LBSpider
from bukvoed import BukvoedSpider

process = CrawlerProcess()
process.crawl(BukvoedSpider)
process.start()