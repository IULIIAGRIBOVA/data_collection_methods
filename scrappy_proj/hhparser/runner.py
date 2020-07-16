from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from hhparser import settings
from hhparser.spiders.hhru import HhruSpider
from hhparser.spiders.superjobru import SuperjobruSpider


if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(HhruSpider)
    process.crawl(SuperjobruSpider)

    process.start()
