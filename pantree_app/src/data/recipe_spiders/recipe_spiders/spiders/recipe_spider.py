import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from recipe_spiders.items import RecipeSpidersItem


class NYTSpider(scrapy.Spider):
    name = "nyt"

    start_urls = [
        'https://cooking.nytimes.com/recipes/146-green-beans-with-ginger-and-garlic'
    ]

    def parse(self, response):
        recipe = RecipeSpidersItem()
        recipe['title'] = response.xpath("//meta[@property='og:title']/@content").extract()[0],
        recipe['img'] = response.xpath("//meta[@property='og:image']/@content").extract()[0],
        recipe['url'] = response.request.url,
        recipe['ings'] = ",".join([x.strip() for x in response.xpath("//span[@class='ingredient-name']/text()").extract()])
        yield recipe
        # yield {
        #         'title' : response.xpath("//meta[@property='og:title']/@content").extract()[0],
        #         'img' : response.xpath("//meta[@property='og:image']/@content").extract()[0],
        #         'url': response.request.url,
        #         'ings' : ",".join([x.strip() for x in response.xpath("//span[@class='ingredient-name']/text()").extract()])
        # }

        next_page = [x for x in response.xpath("//a/@href").extract() if x.startswith(r'/recipes/')][1]
        anchors = [x for x in response.xpath("//a/@href").extract() if x.startswith(r'/recipes/')]
        if next_page is not None:
            yield from response.follow_all(anchors, callback=self.parse)
            # yield response.follow(next_page, callback=self.parse)
            # yield from response.follow_all(css='ul.pager a', callback=self.parse)



settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(NYTSpider)
process.start()