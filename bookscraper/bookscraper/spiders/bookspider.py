import scrapy

from ..items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()

            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url, callback=self.parse_book_page, meta={"proxy":"http://user-asdas3a4545:12345678@gate.smartproxy.com:7000"})

        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse, meta={"proxy":"http://user-asdas3a4545:12345678@gate.smartproxy.com:7000"})

    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        bookItem = BookItem()

        bookItem['url'] = response.url,
        bookItem['title'] = response.css('.product_main h1::text').get(),
        bookItem['upc'] = table_rows[0].css("td::text").get(),
        bookItem['product_type'] = table_rows[1].css('td::text').get(),
        bookItem['price_excl_tax'] = table_rows[2].css('td::text').get(),
        bookItem['price_incl_tax'] = table_rows[3].css('td::text').get(),
        bookItem['tax'] = table_rows[4].css('td::text').get(),
        bookItem['availability'] = table_rows[5].css('td::text').get(),
        bookItem['num_reviews'] = table_rows[6].css('td::text').get(),
        bookItem['stars'] = response.css('p.star-rating').attrib['class'],
        bookItem['category'] = response.xpath(
            "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        bookItem['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        bookItem['price'] = response.css('p.price_color::text').get(),

        yield bookItem
