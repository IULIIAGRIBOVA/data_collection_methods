import scrapy
from scrapy.http import HtmlResponse
from leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LermerlSpider(scrapy.Spider):
    name = 'lermerl'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://kaliningrad.leroymerlin.ru/catalogue/kaktusy-i-sukkulenty/']

    #def __init__(self, search, city):
    #    self.start_urls = [f'https://www.avito.ru/{city}?q={search}']

    def parse(self, response):
        ads_links = response.xpath("//a[@class='link-wrapper']")
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def defenition_list_to_dict(self, value):
        # print(type(value))
        deflist = {}
        for defenition_item in value:
            term = defenition_item.xpath(".//dt[@class='def-list__term']/text()").extract_first()
            definition = defenition_item.xpath(".//dd[@class='def-list__definition']/text()").extract_first()
            definition = definition.strip()
            deflist.update({term:definition})
        return deflist


    def parse_ads(self, response):
        def_list = response.xpath("//div[@class = 'def-list__group']")
        def_list = self.defenition_list_to_dict(def_list)
        price = response.xpath("//span[@slot = 'price']/text()").extract_first()

        loader = ItemLoader(item=LeroymerlinItem(),response=response)
        loader.add_xpath('name',"//h1/text()")
        loader.add_xpath('photos',"//uc-pdp-media-carousel/img/@src")
        loader.add_value('price', price)
        loader.add_value('url', response.url)
        loader.add_value('def_list', def_list)
        yield loader.load_item()

