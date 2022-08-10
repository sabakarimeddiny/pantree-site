import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from recipe_spiders.items import RecipeSpidersItem

class NYTSpider(scrapy.Spider):
    name = "nyt"

    start_urls = [
        'https://cooking.nytimes.com/'
    ]
    allowed_domains = [
        'cooking.nytimes.com'
    ]

    def parse(self, response):
        recipe = RecipeSpidersItem()
        recipe['title'] = response.xpath("//meta[@property='og:title']/@content").extract()[0]
        recipe['img'] = response.xpath("//meta[@property='og:image']/@content").extract()[0]
        recipe['url'] = response.request.url.split('#')[0].split('&')[0].split('?')[0]
        recipe['ings'] = ",".join([x.strip() for x in response.xpath("//span[@class='ingredient-name']/text()").extract()])
        if recipe['ings'] != '':
            yield recipe

        anchors = [x for x in response.xpath("//a/@href").extract()]   
        if anchors != []:
            yield from response.follow_all(anchors, callback=self.parse)

class Food52Spider(scrapy.Spider):
    name = "food52"

    start_urls = [
        'https://food52.com/recipes/'
    ]
    allowed_domains = [
        'food52.com'
    ]

    def parse(self, response):
        recipe = RecipeSpidersItem()
        recipe['title'] = response.xpath("//meta[@property='og:title']/@content").extract()[0]
        recipe['img'] = response.xpath("//meta[@property='og:image']/@content").extract()[0]
        recipe['url'] = response.request.url.split('#')[0].split('&')[0].split('?')[0]
        recipe['ings'] = ",".join([x.strip() for x in response.xpath("//div[@class='recipe__list recipe__list--ingredients']/ul/li/text()").extract()])
        if recipe['ings'] != '':
            yield recipe

        anchors = [x for x in response.xpath("//a/@href").extract()]   
        if anchors != []:
            yield from response.follow_all(anchors, callback=self.parse)

class LiquorSpider(scrapy.Spider):
    name = "liquor"

    start_urls = [
        'https://www.liquor.com/recipes/'
    ]
    allowed_domains = [
        'liquor.com'
    ]

    def parse(self, response):
        recipe = RecipeSpidersItem()
        recipe['title'] = response.xpath("//meta[@property='og:title']/@content").extract()[0]
        recipe['img'] = response.xpath("//meta[@property='og:image']/@content").extract()[0]
        recipe['url'] = response.request.url.split('#')[0].split('&')[0].split('?')[0]
        recipe['ings'] = ",".join([x.strip() for x in response.xpath("//section[@class='comp section--ingredients section']/div/ul/li/text()").extract()])
        if recipe['ings'] != '':
            yield recipe

        anchors = [x for x in response.xpath("//a/@href").extract()]   
        if anchors != []:
            yield from response.follow_all(anchors, callback=self.parse)

class BonAppetitSpider(scrapy.Spider):
    name = "ba"

    start_urls = [
        'https://www.bonappetit.com/recipe/'
    ]
    allowed_domains = [
        'bonappetit.com'
    ]

    def parse(self, response):
        recipe = RecipeSpidersItem()
        recipe['title'] = response.xpath("//meta[@property='og:title']/@content").extract()[0]
        recipe['img'] = response.xpath("//meta[@property='og:image']/@content").extract()[0]
        recipe['url'] = response.request.url.split('#')[0].split('&')[0].split('?')[0]
        recipe['ings'] = ",".join([x.strip() for x in response.xpath("//div[@class='BaseWrap-sc-UABmB BaseText-fETRLB Description-dTsUqb hkSZSE kBLSTT gmvWnL']/text()").extract()])
        if recipe['ings'] != '':
            yield recipe

        anchors = [x for x in response.xpath("//a/@href").extract()]   
        if anchors != []:
            yield from response.follow_all(anchors, callback=self.parse)

class EpicuriousSpider(scrapy.Spider):
    name = "epicurious"

    start_urls = [
        'https://www.epicurious.com/recipes/'
    ]
    allowed_domains = [
        'epicurious.com'
    ]

    def parse(self, response):
        recipe = RecipeSpidersItem()
        recipe['title'] = response.xpath("//meta[@property='og:title']/@content").extract()[0]
        recipe['img'] = response.xpath("//meta[@property='og:image']/@content").extract()[0]
        recipe['url'] = response.request.url.split('#')[0].split('&')[0].split('?')[0]
        recipe['ings'] = ",".join([x.strip() for x in response.xpath("//div[@class='BaseWrap-sc-UABmB BaseText-fETRLB Description-dTsUqb hkSZSE kYypVx gmvWnL']/text()").extract()])
        if recipe['ings'] != '':
            yield recipe

        anchors = [x for x in response.xpath("//a/@href").extract()]   
        if anchors != []:
            yield from response.follow_all(anchors, callback=self.parse)

class AllRecipesSpider(scrapy.Spider):
    name = "allrecipes"

    start_urls = [
        'https://www.allrecipes.com/'
    ]
    allowed_domains = [
        'allrecipes.com'
    ]

    def parse(self, response):
        recipe = RecipeSpidersItem()
        recipe['title'] = response.xpath("//meta[@property='og:title']/@content").extract()[0]
        recipe['img'] = response.xpath("//meta[@property='og:image']/@content").extract()[0]
        recipe['url'] = response.request.url.split('#')[0].split('&')[0].split('?')[0]
        recipe['ings'] = ",".join([x.strip() for x in response.xpath("//span[@class='ingredients-item-name elementFont__body']/text()").extract()])
        if recipe['ings'] != '':
            yield recipe

        anchors = [x for x in response.xpath("//a/@href").extract()]   
        if anchors != []:
            yield from response.follow_all(anchors, callback=self.parse)

class SeriousEatsSpider(scrapy.Spider):
    name = "seriouseats"

    start_urls = [
        'https://www.seriouseats.com/'
    ]
    allowed_domains = [
        'seriouseats.com'
    ]

    def parse(self, response):
        recipe = RecipeSpidersItem()
        recipe['title'] = response.xpath("//meta[@property='og:title']/@content").extract()[0]
        recipe['img'] = response.xpath("//meta[@property='og:image']/@content").extract()[0]
        recipe['url'] = response.request.url.split('#')[0].split('&')[0].split('?')[0]
        recipe['ings'] = ",".join([x.strip() for x in response.xpath("//li[@class='simple-list__item js-checkbox-trigger ingredient text-passage']/text()").extract()])
        if recipe['ings'] != '':
            yield recipe

        anchors = [x for x in response.xpath("//a/@href").extract()]   
        if anchors != []:
            yield from response.follow_all(anchors, callback=self.parse)

class SmittenKitchenSpider(scrapy.Spider):
    name = "smittenkitchen"

    start_urls = [
        'https://smittenkitchen.com/recipes/'
    ]
    allowed_domains = [
        'smittenkitchen.com'
    ]
    # custom_settings = {
    #     'DEPTH_LIMIT' : 2
    # }

    def parse(self, response):
        recipe = RecipeSpidersItem()
        recipe['title'] = response.xpath("//meta[@property='og:title']/@content").extract()[0]
        recipe['img'] = response.xpath("//meta[@property='og:image']/@content").extract()[0]
        recipe['url'] = response.xpath("//link[@rel='canonical']/@href").get() #response.request.url.split('#')[0].split('&')[0].split('?')[0]
        recipe['ings'] = ",".join([x.strip() for x in response.xpath("//li[@class='jetpack-recipe-ingredient p-ingredient ingredient']/text()").extract()])
        if recipe['ings'] != '':
            yield recipe
        anchors = [x for x in response.xpath("//a/@href").extract() if '?' not in x and '#' not in x and '&' not in x]   
        if anchors != []:
            yield from response.follow_all(anchors, callback=self.parse)

class FoodAndWine(scrapy.Spider):
    name = "foodandwine"

    start_urls = [
        'https://www.foodandwine.com/recipes/'
    ]
    allowed_domains = [
        'foodandwine.com'
    ]

    def parse(self, response):
        recipe = RecipeSpidersItem()
        recipe['title'] = response.xpath("//meta[@property='og:title']/@content").extract()[0]
        recipe['img'] = response.xpath("//meta[@property='og:image']/@content").extract()[0]
        recipe['url'] = response.xpath("//link[@rel='canonical']/@href").get() #response.request.url.split('#')[0].split('&')[0].split('?')[0]
        recipe['ings'] = ",".join([x.strip() for x in response.xpath("//span[@class='ingredients-item-name elementFont__body']/text()").extract()])
        if recipe['ings'] != '':
            yield recipe
        anchors = [x for x in response.xpath("//a/@href").extract() if '?' not in x and '#' not in x and '&' not in x]   
        if anchors != []:
            yield from response.follow_all(anchors, callback=self.parse)

class Delish(scrapy.Spider):
    name = "delish"

    start_urls = [
        'https://www.delish.com/cooking/',
        'https://www.delish.com/best-cocktail-recipes/'
    ]
    allowed_domains = [
        'delish.com'
    ]

    def parse(self, response):
        recipe = RecipeSpidersItem()
        try:
            recipe['title'] = response.xpath("//meta[@property='og:title']/@content").extract()[0]
            recipe['img'] = response.xpath("//meta[@property='og:image']/@content").extract()[0]
            recipe['url'] = response.xpath("//link[@rel='canonical']/@href").get() #response.request.url.split('#')[0].split('&')[0].split('?')[0]
            recipe['ings'] = ",".join([x.strip() for x in response.xpath("//span[@class='ingredient-description']/p/text()").extract()])
            if recipe['ings'] != '':
                yield recipe
        except IndexError:
            pass
        anchors = [x for x in response.xpath("//a/@href").extract() if '?' not in x and '#' not in x and '&' not in x]   
        if anchors != []:
            yield from response.follow_all(anchors, callback=self.parse)