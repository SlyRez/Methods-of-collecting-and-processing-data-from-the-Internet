import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    # фильтровал по требуемому опыту
    start_urls = ['https://spb.hh.ru/search/vacancy?fromSearchLine=true&text=python&area=2&experience=between1And3&search_field=description&search_field=company_name&search_field=name',
                  'https://spb.hh.ru/search/vacancy?fromSearchLine=true&text=python&area=2&experience=between3And6&search_field=description&search_field=company_name&search_field=name',
                  'https://spb.hh.ru/search/vacancy?fromSearchLine=true&text=python&area=2&experience=noExperience&search_field=description&search_field=company_name&search_field=name',
                  'https://spb.hh.ru/search/vacancy?fromSearchLine=true&text=python&area=2&experience=moreThan6&search_field=description&search_field=company_name&search_field=name'
                  ]

    def parse (self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse (self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[@class='vacancy-salary']/span/text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)