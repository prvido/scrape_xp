import scrapy
from scrapy.crawler import CrawlerProcess
import re

class StockSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = ['https://conteudos.xpi.com.br']

    ativos = [linha.strip() for linha in open(r'C:\Users\prvid\code\scrapy\scrape_xp\scrape_xp\ativos\stocks.txt', 'r')]

    ativo_recomendados = []

    contador = -1

    def parse(self, response):

    
        if self.contador == -1:
            self.ativos_recomendados = response.css('div.box-produtos h4::text').getall()
        
        else:
            ativo = self.ativos[self.contador]
            descricao = response.css('h1::text').get()
            
            try:
                risco = response.css('span.genius-risk::text').get().replace('\n', '').replace(' ', '')
                classe_risco = response.css('span.genius-risk::attr(class)').get()[19:].capitalize()
                recomendacao = response.css('span.recomendacao::text').get().capitalize()
                case = re.sub('<.*?>', '', response.css('article p').get())

                try:
                    preco_alvo = float(response.css('li.item-dado-produto::text').getall()[3].replace('\n', '').replace(' ', '').replace('R$', '').replace(',', '.'))
                except ValueError:
                    preco_alvo = 0

            except AttributeError:
                risco = 0
                classe_risco = ''
                recomendacao = ''
                preco_alvo = 0
                case = ''
                
            
            is_recomendado = ativo in self.ativos_recomendados
            
            has_valuation = preco_alvo != 0


            yield {
                'ativo': ativo,
                'descricao': descricao,
                'case': case,
                'preco_alvo': preco_alvo,
                'has_valuation': has_valuation,
                'risco': risco,
                'classe_risco': classe_risco,
                'recomendacao': recomendacao,
                'is_recomendado': is_recomendado
            }
        
        self.contador = self.contador + 1

        if self.contador < len(self.ativos):
            next_page = 'https://conteudos.xpi.com.br/acoes/' + self.ativos[self.contador]
        
            yield response.follow(next_page, callback=self.parse)


process = CrawlerProcess(
                    settings = {
                        'FEEDS': {
                            'stocks.json': {'format': 'json'}
                        }
                    }
                )

process.crawl(StockSpider)
process.start()