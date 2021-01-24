import scrapy

class QuoteSpider(scrapy.Spider):
    name = 'books'

    def start_requests(self):
        urls = [
        'http://books.toscrape.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        page = response.url.split('/')
        filename = 'book-%s.html' % page

        for b in response.css('div.row article.product_pod'):
            img = b.css(' .image_container img::attr(src)').get()
            name = b.css('h3 a::text').get()
            price = b.css('p.price_color::text').get()

            yield {
            'img':img,
            'name':name,
            'price':price
            }

            next_page = response.css('li.next a::attr(href)').get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
