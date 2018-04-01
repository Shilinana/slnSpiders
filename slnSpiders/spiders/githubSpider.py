import scrapy
import logging
from slnSpiders.items import SlnspidersItem

class GithubSpider(scrapy.Spider):
    name = 'github'
    allow_domains = ["github.com"]
    base_url = "https://github.com"
    start_urls = [
      "https://github.com/explore",
    ]
    def parse(self, response):
      repo_urls = []
      #//div[contains(@class, 'Collection')]//article
      for selector in response.xpath("//body//div[4]//div[contains(@class, 'Collection')]//article//a"):
        for i in selector.xpath('@href').extract():
          if 'network' not in i:
            url = self.base_url + i
            repo_urls.append(url)
            self.logger.info(url)