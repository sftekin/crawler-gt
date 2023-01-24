import csv

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import GtcrawlerItem
from scrapy.http import TextResponse
import requests
import time
from cleantext import clean

# https://www.cc.gatech.edu/people/faculty
# https://www.cc.gatech.edu/people/jacob-abernethy


class GTSpider(CrawlSpider):
    name = "gts"
    allowed_domains = ["cc.gatech.edu"]
    start_urls = ["https://www.cc.gatech.edu"]
    text_limit = 5000

    url_count = 0
    keyword_count = 0

    rules = (
        Rule(LinkExtractor(allow="people"), callback="parse_page", follow=True),
    )

    def parse_page(self, response, **kwargs):
        raw_url = response.url
        page_name = raw_url.split("/")[-1]
        is_not_valid = self.checker(name=page_name)

        # increase the url count even though it is not valid
        self.url_count += 1

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
            p_text = " ".join(resp.css("p::text").extract())
            s_text = " ".join(resp.css("span::text").extract())
            p_text = self.strip_text(p_text, self.text_limit)
            s_text = self.strip_text(s_text, self.text_limit)

            # record the number of keywords that are scrapped
            self.keyword_count += len(p_text.split(" ")) + len(s_text.split(" "))

            item["content"] = {
                "paragraph": p_text,
                "span": s_text
            }

        # record some analysis
        self.record()

        yield item

    def record(self):
        with open("stats.csv", "a+", newline='\n') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([time.time(), self.url_count, self.keyword_count])

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

    @staticmethod
    def strip_text(text, limit):
        replace_elements = ["\t", "\n", "[", "]"]
        stripped = text.strip()
        for el in replace_elements:
            stripped = stripped.replace(el, "")
        clean_text = clean(stripped,
                           fix_unicode=True,  # fix various unicode errors
                           to_ascii=True,  # transliterate to closest ASCII representation
                           lower=True,  # lowercase text
                           no_line_breaks=True,  # fully strip line breaks as opposed to only normalizing them
                           no_urls=False,  # replace all URLs with a special token
                           no_emails=False,  # replace all email addresses with a special token
                           no_phone_numbers=False,  # replace all phone numbers with a special token
                           no_numbers=False,  # replace all numbers with a special token
                           no_digits=False,  # replace all digits with a special token
                           no_currency_symbols=False,  # replace all currency symbols with a special token
                           no_punct=True,  # remove punctuations
                           replace_with_punct="",  # instead of removing punctuations you may replace them
                           replace_with_url="<URL>",
                           replace_with_email="<EMAIL>",
                           replace_with_phone_number="<PHONE>",
                           replace_with_number="<NUMBER>",
                           replace_with_digit="0",
                           replace_with_currency_symbol="<CUR>",
                           lang="en")
        clean_text = clean_text[:limit]
        return clean_text

