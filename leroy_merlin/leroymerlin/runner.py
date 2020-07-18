from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


from leroymerlin.spiders.lermerl import LermerlSpider
from leroymerlin import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LermerlSpider,search='Mercedes gle coupe',city='izhevsk')

    process.start()