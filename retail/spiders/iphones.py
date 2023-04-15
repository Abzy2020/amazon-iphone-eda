import scrapy
import asyncio

# scrapes amazon for iphone data
class RetailSpider(scrapy.Spider):

    name = 'phones'

    def __init__(self):
        self.current = 2


    def start_requests(self):
        url = 'https://www.amazon.com/s?k=iphone'
        headers = {
            #headers
        }
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={'pyppeteer': True})


    #scrapy runspider -o phones.jsonl phones.py
    def parse(self, response):
        total_pages = response.xpath('//*[@class="a-pagintation"]/li[last()-1]/text()').get()
        current_page = response.xpath('//*[aria-current="page"]/text()').get()

        if total_pages and current_page:
            if int(current_page) == 1:
                for i in range(2, int(total_pages) + 1):
                    url = f'https://www.amazon.com/s?k=iphone&page={i}&qid=1679636328&ref=sr_pg_2'
                    yield scrapy.Request(url)

        for phone in response.css('div.sg-col.sg-col-4-of-12.sg-col-8-of-16.sg-col-12-of-20.sg-col-12-of-24.s-list-col-right'):
            title = phone.css('span.a-size-medium.a-color-base.a-text-normal::text').get()
            stars = phone.css('div.a-row.a-size-small span.a-size-base::text').get()
            total_reviews = phone.css('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style span.a-size-base.s-underline-text::text').get()
            price = phone.css('span.a-price span.a-offscreen::text').get()
            yield {
                'title': title,
                'stars': stars,
                'total_reviews': total_reviews,
                'price': price
            }
        # next_page = response.xpath('//*[@class="a-pagintation"]/li[last()]/a/text()').get()
        # if next_page:
        #     yield scrapy.Request(response.urljoin(next_page))