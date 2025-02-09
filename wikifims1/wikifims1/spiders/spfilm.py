import scrapy
import re

class SpfilmSpider(scrapy.Spider):
    name = 'spfilm'
    def start_requests(self):
        URL = 'https://ru.wikipedia.org/w/index.php?title=Категория:Фильмы_по_алфавиту'        
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
        search_urls = []
        for selector in response.css("div.mw-category-group ul li a::attr(href)"):
            yield response.follow(url=selector.getall()[0], callback=self.parse_films)

        for selector in response.css("div.ts-module-Индекс_категории-container ul li a::attr(href)"):   
            search_urls.append(str(selector.getall()[0]))

        for urls in search_urls:
            yield response.follow(url=urls, callback=self.parse_films_urls)
    
    def parse_films_urls(self, response):
        for selector in response.css("div.mw-category-group ul li a::attr(href)"):
            yield response.follow(url=selector.getall()[0], callback=self.parse_films)

    def parse_films(self, response):
        title = response.xpath(
            '//h1[@id="firstHeading"]//span[@class="mw-page-title-main"]/text()'
        ).get()

        genre = response.xpath(
            '//table[contains(@class, "infobox")]'
            '//th[contains(.,"Жанр")]/following-sibling::td//text()'
            ).getall()
        genre = ''.join(genre).strip()
        genre = re.sub(r'\[\d+\]', '', genre)
        
        director = response.xpath(
            '//table[contains(@class, "infobox")]'
            '//th[contains(.,"Режиссёр") or contains(.,"Режиссер")]'
            '/following-sibling::td'
            '//text()[not(ancestor::sup) and not(ancestor::style) and not(ancestor::script)]'
            ).getall()
        director = ''.join(director).strip()
        director = re.sub(r'\[\d+\]', '', director)

        country = response.xpath(
            '//table[contains(@class, "infobox")]'
            '//th[contains(.,"Страна")]/following-sibling::td//text()'
            ).getall()
        country = ''.join(country).strip()
        country = re.sub(r'\[\d+\]', '', country)

        year = response.xpath(
            '//table[contains(@class, "infobox")]'
            '//th[contains(.,"Год")]/following-sibling::td//text()'
            ).getall()
        year = ''.join(year).strip()
        year = re.sub(r'\[\d+\]', '', year)

        yield {'title': title,
        'genre': genre,
        'director': director,
        'country': country,
        'year': year
        }








        


             