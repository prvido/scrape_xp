import scrapy
import re

class StockSpider(scrapy.Spider):
    name = 'stocks'
    contador = 0
    ativos = [linha.strip() for linha in open(r'C:\Users\prvid\code\scrapy\scrape_xp\scrape_xp\ativos\stocks.txt', 'r')]
    start_urls = [f'https://conteudos.xpi.com.br/acoes/{ativos[contador]}']

    
    def parse(self, response):


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

        has_valuation = preco_alvo != 0


        yield {
            'ativo': ativo,
            'descricao': descricao,
            'preco_alvo': preco_alvo,
            'has_valuation': has_valuation,
            'risco': risco,
            'classe_risco': classe_risco,
            'recomendacao': recomendacao,
            'case': case
        }

        self.contador = self.contador + 1

        if self.contador < len(self.ativos):
            next_page = 'https://conteudos.xpi.com.br/acoes/' + self.ativos[self.contador]

        yield response.follow(next_page, callback=self.parse)