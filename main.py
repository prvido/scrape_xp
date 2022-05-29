import os
from scrape_xp.spiders.stock_spider import StockSpider
from scrapy.crawler import CrawlerProcess

stock_process = CrawlerProcess(
                    settings = {
                        'FEEDS': {
                            'stocks.json': {'format': 'json'}
                        }
                    }
                )

try:
    os.remove(r'C:\Users\prvid\code\scrapy\scrape_xp\stocks.json')
except FileNotFoundError:
    pass

stock_process.crawl(StockSpider)
stock_process.start()