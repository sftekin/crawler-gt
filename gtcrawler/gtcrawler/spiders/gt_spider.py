import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# https://www.cc.gatech.edu/people/faculty
# https://www.cc.gatech.edu/people/jacob-abernethy


class GTSpider(CrawlSpider):
    name = "gts"
    allowed_domains = ["cc.gatech.edu"]
    start_urls = ["https://www.cc.gatech.edu"]

    rules = (
        Rule(LinkExtractor(), callback="parse_page", follow=True),
    )

    def parse_page(self, response, **kwargs):
        yield {
            "url": response.url
        }
