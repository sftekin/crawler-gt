import scrapy
from ..items import QuotetutorialItem


class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com"
    ]

    def parse(self, response, **kwargs):

        items = QuotetutorialItem()

        all_div_quotes = response.css("div.quote")

        for quote in all_div_quotes:
            title = quote.css("span.text::text").extract()
            author = quote.css(".author::text").extract()
            tags = quote.css(".tag::text").extract()

            items['title'] = title
            items['author'] = author
            items['tags'] = tags

            yield items

        next_page = response.css("li.next a").attrib['href']
        next_page = self.start_urls[0] + next_page
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
