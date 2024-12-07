from scrapy.crawler import CrawlerProcess
from chitaigorod import CGSpider
process = CrawlerProcess()

CGSpider.set_pipeline("Bookparser.CSVPipeline")
CGSpider.set_query("Атлант Расправил Плечи")
process.crawl(CGSpider)
process.start()
# Отправит найденное в эксельку CSVBooks.csv