import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from recipe_spiders.spiders.recipe_spider import *
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging


# import sys    
# if "twisted.internet.reactor" in sys.modules:
#     del sys.modules["twisted.internet.reactor"]

# settings = get_project_settings()
# process = CrawlerProcess(settings)
# process = CrawlerProcess()
# process.crawl(NYTSpider)
# process.crawl(BonAppetitSpider)
# process.start()

configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)
runner.crawl(NYTSpider)
runner.crawl(Food52Spider)
runner.crawl(LiquorSpider)
runner.crawl(BonAppetitSpider)
runner.crawl(EpicuriousSpider)
runner.crawl(AllRecipesSpider)
runner.crawl(SeriousEatsSpider)
runner.crawl(SmittenKitchenSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run() 