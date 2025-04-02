import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            title = book.css("h3 a::attr(title)").get()
            price = book.css(".price_color::text").get()
            rating = book.css("p.star-rating::attr(class)").get().split()[-1]

            yield {
                "title": title,
                "price": price,
                "rating": rating
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
