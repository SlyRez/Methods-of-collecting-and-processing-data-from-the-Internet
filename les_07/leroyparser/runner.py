from scrapy.crawler import CrawlerProcess
from leroyparser import settings
from scrapy.settings import Settings
from leroyparser.spiders.leroymerlinru import LeroymerlinruSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinruSpider)
    process.start()