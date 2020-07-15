import scrapy
from hhparser.items import HhparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://kaliningrad.hh.ru/search/vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page=0']



    def parse(self, response):

        vacancy_block = response.xpath("//div[@class='vacancy-serp']")
        vacancy_list = vacancy_block.xpath(".//div[@class='vacancy-serp-item ']")
        for vacancy in vacancy_list:
            name_vac = vacancy.css('a.bloko-link::text').extract_first()
            salary_vac = vacancy.xpath("//span[@data-qa='vacancy-serp__vacancy-compensation']/text()").extract_first()
            vacancy_href = vacancy.css('a.bloko-link::attr(href)').extract_first()

            yield HhparserItem(name=name_vac, salary=salary_vac, site = 'hh.ru', link = vacancy_href)

        next_button = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()

        yield response.follow(next_button, callback = self.parse)
        pass

