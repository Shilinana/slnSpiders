import scrapy
import logging
from scrapy.loader import ItemLoader
from slnSpiders.items import GithubCatagaryItem
class GithubSpider(scrapy.Spider):
    name = 'github'
    allow_domains = ["github.com"]
    base_url = "https://github.com"
    start_urls = [
      "https://github.com/explore",
    ]
    all_the_repo_info = {}
    def parse(self, response):
      req = []
      for selector in response.xpath("//body//div[4]//h2//a[contains(@class, 'link-gray-dark')]"):
        for i in selector.xpath('@href').extract():
          catagart_url = self.base_url + i
          yield scrapy.Request(catagart_url, callback=self.parse_categary)

      for url in response.xpath("/body//div[4]//div[contains(@class, 'py-4')]//a//@href").extract():
        r = self.base_url + url
        yield scrapy.Request(r, callback=self.parse_categary)

    def parse_categary(self, response):
      page = response.url.split("/")[-1]
      self.all_the_repo_info[page] = {
        'repo_urls': [],
      }
      for selector in response.xpath("//body//div[4]//div[1]//div[1]//ol[contains(@class, 'repo-list')]//h3//a"):
        for url in selector.xpath('@href').extract():
          self.all_the_repo_info[page]['repo_urls'].append(self.base_url + url)
      for selector in response.xpath("//body//div[4]//div[1]//div[1]//article//h1//a"):
        for url in selector.xpath('@href').extract():
          self.all_the_repo_info[page]['repo_urls'].append(self.base_url + url)
    # def parse_repo_info(self, response):
