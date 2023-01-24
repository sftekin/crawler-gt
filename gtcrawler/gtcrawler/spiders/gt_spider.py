import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import GtcrawlerItem
from scrapy.http import TextResponse
import requests

# https://www.cc.gatech.edu/people/faculty
# https://www.cc.gatech.edu/people/jacob-abernethy


class GTSpider(CrawlSpider):
    name = "gts"
    allowed_domains = ["cc.gatech.edu"]
    start_urls = ["https://www.cc.gatech.edu"]

    rules = (
        Rule(LinkExtractor(allow="people"), callback="parse_page", follow=True),
    )

    # def _parse(self, response, **kwargs):
    #     print(response.url)
    #     return super()._parse(response, **kwargs)

    def parse_page(self, response, **kwargs):
        raw_url = response.url
        page_name = raw_url.split("/")[-1]
        is_not_valid = self.checker(name=page_name)

        if is_not_valid:
            # exit here if it is not valid
            return None

        item = GtcrawlerItem()
        item["name"] = response.css("h1.page-title span::text").get()
        item["title"] = response.css("h6::text").get()
        item["contacts"] = response.css("p.card-block__text a::text").extract()
        item["research_area"] = "".join(response.css("p.card-block__text::text").extract()).strip()

        next_page = self.get_webpage(item["contacts"])
        if next_page is not None:
            resp = requests.get(next_page)
            resp = TextResponse(body=resp.content, url=next_page)
            item["webpage_body"] = resp.css("::text").extract()

        yield item

    @staticmethod
    def checker(name):
        checks = [
            len(name) <= 1,
            "page" in name,
            "advisory-board" == name,
            "phd" == name,
            "people" == name,
            "staff" == name,
            "faculty" == name
        ]
        return any(checks)

    @staticmethod
    def get_webpage(contacts):
        webpage = None
        for c in contacts:
            if "http" in c:
                webpage = c
        return webpage

