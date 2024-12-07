from scrapy.crawler import CrawlerProcess
from mif import MIFSpider
from chitaigorod import CGSpider
from labirint import LBSpider
from bukvoed import BukvoedSpider

process = CrawlerProcess()
CGSpider.set_query("Атлант Расправил Плечи")
#BukvoedSpider.set_pipeline("parser.DBPipeline")
process.crawl(CGSpider)
process.start()