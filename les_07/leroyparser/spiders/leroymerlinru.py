import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/otdelochnye-pokrytiya-dlya-pola/']

    def parse(self, response: HtmlResponse):
        next_page_link = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)

        products_links = response.xpath("//a[@data-qa='product-name']/@href").getall()
        for link in products_links:
            yield response.follow(link, callback=self.parse_product_info)

    def parse_product_info(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_xpath("title", "//h1/text()")
        loader.add_xpath("price", "//span[@slot='price']/text()")
        loader.add_xpath("photos", "//img[@alt='product image']/@src")
        yield loader.load_item()