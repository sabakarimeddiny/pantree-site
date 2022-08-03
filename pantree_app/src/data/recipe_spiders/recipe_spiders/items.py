# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class RecipeSpidersItem(Item):
    title = Field()
    img = Field()
    url = Field()
    ings = Field()