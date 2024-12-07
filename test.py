from scrapy.crawler import CrawlerProcess
from chitaigorod import CGSpider

process = CrawlerProcess()
CGSpider.set_query("Атлант Расправил Плечи")
#BukvoedSpider.set_pipeline("parser.DBPipeline")
process.crawl(CGSpider)
process.start()