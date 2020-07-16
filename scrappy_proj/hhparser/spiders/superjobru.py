

import scrapy
from hhparser.items import HhparserItem

class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    main_link = 'https://russia.superjob.ru'

    def parse(self, response):
        vacancy_block = response.xpath("//div[@class='_1ID8B']")
        vacancy_list = vacancy_block.xpath(".//div[@class='_3zucV _1fMKr undefined _1NAsu']")

        for vacancy in vacancy_list:
            vacancy_div = vacancy.xpath(".//div[@class='jNMYr GPKTZ _1tH7S']")
            if vacancy_div != None:
               name_vac = vacancy_div.css('a::text').extract_first()

               vacancy_href = vacancy.css('a::attr(href)').extract_first()
               salary_vac = vacancy_block.xpath(".//span[@class='_3mfro _2Wp8I PlM3e _2JVkc _2VHxz']/text()").extract_first()
               yield HhparserItem(name=name_vac, salary=salary_vac, site = 'superjob.ru', link = vacancy_href)


        next_button = response.css('a.f-test-button-dalshe::attr(href)').extract_first()
        yield response.follow(self.main_link+next_button, callback = self.parse)



