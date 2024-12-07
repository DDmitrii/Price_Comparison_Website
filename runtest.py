from chitaigorod import CGSpider
from scrapy.crawler import CrawlerProcess
process = CrawlerProcess()
CGSpider.set_pages_amount(1)
process.crawl(CGSpider)
process.start()