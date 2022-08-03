# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import sqlite3
# This pipeline takes the Item and stuffs it into scrapedata.db

class RecipeSpidersPipeline(object):
    def __init__(self):
        # Possible we should be doing this in spider_open instead, but okay
        self.connection = sqlite3.connect('./scrapedata.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS recipes USING FTS5(title, img, url, ingredients)")

    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):
        self.cursor.execute("select * from recipes where url=?", (item['url'],))
        result = self.cursor.fetchone()
        if result:
            pass
            # logging.INFO("Item already in database: %s" %str(item['title']), level=logging.DEBUG)
        else:
            self.cursor.execute(
                "INSERT INTO recipes VALUES (?, ?, ?, ?)",
                    (str(item['title']), str(item['img']), str(item['url']), str(item['ings']))
            )
            self.connection.commit()

            # logging.INFO("Item stored : %s" %str(item['title']), level=logging.DEBUG)
        return item

    def handle_error(self, e):
        logging.ERROR(e)

