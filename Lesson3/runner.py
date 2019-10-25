from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from hh_vac import settings
from hh_vac.spiders.hh_vac_sp import HhVacSpSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhVacSpSpider)
    process.start()

