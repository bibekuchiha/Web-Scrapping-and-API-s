import scrapy

class QuoteSpider(scrapy.Spider):
    name = 'goodread'

    def start_requests(self):
        urls = [
        'https://www.goodreads.com/quotes']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split('/')
        filename = 'quotes-%s.html' % page

        for q in response.css('div.quoteDetails'):
            quote = q.css('div.quoteText::text').get()
            author = q.css('span.authorOrTitle::text').get()
            tags = q.css('div.greyText a::text').getall()
            likes = q.css('div.right a.smallText::text').get()

            yield {
            'quotes':quote,
            'author': author,
            'tags': tags,
            'likes':likes
            }
        next_page = response.css('div a.next_page::attr(href)').get()
        if next_page is not None:
              next_page = response.urljoin(next_page)
              yield scrapy.Request(next_page, callback=self.parse)
