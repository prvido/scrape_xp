import os
from scrape_xp.spiders.stock_spider import StockSpider
from scrapy.crawler import CrawlerProcess
import pandas as pd

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

dados = pd.read_json(r'C:\Users\prvid\code\scrapy\scrape_xp\stocks.json', encoding='utf-8-sig')

dados.to_csv(r'C:\Users\prvid\code\scrapy\scrape_xp\stocks.csv', sep=';', encoding='utf-8-sig', decimal=',')