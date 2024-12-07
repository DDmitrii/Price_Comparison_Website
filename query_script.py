from scrapy.crawler import CrawlerProcess
from .. import chitaigorod
from chitaigorod import CGSpider
process = CrawlerProcess()
CGSpider.set_query("Атлант Расправил Плечи")
process.crawl(CGSpider)
process.start()
# Отправит найденное в эксельку CSVBooks.csv