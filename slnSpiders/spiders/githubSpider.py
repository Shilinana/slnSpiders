import scrapy
import logging
from scrapy.loader import ItemLoader
from slnSpiders.items import GithubCategoryItem
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
          category_url = self.base_url + i
          self.logger.info('### category_url: ' + category_url)
          yield scrapy.Request(category_url, callback=self.parse_category)

      for url in response.xpath("//body//div[4]//div[contains(@class, 'py-4')]//a//@href").extract():
        r = self.base_url + url
        self.logger.info('### category_url: ' + r)        
        yield scrapy.Request(r, callback=self.parse_category)

    def parse_category(self, response):
      page = response.url.split("/")[-1]
      self.logger.info('### current_page: ' + page)
      self.all_the_repo_info[page] = {
        'repo_urls': [],
      }
      for selector in response.xpath("//body//div[4]//div[1]//div[1]//ol[contains(@class, 'repo-list')]//h3//a"):
        for url in selector.xpath('@href').extract():
          self.all_the_repo_info[page]['repo_urls'].append(self.base_url + url)
      for selector in response.xpath("//body//div[4]//div[1]//div[1]//article//h1//a"):
        for url in selector.xpath('@href').extract():
          self.all_the_repo_info[page]['repo_urls'].append(self.base_url + url)
      for page in self.all_the_repo_info:
        self.current_page = page
        for url in self.all_the_repo_info[page]['repo_urls']:
          self.logger.info('## current url: ' + url)
          yield scrapy.Request(url, callback=self.parse_repo_info)
    def parse_repo_info(self, response):
      github_item_loader = ItemLoader(item = GithubCategoryItem(), response=response)
      category = response.request.headers.get('Referer', None).split('/')[-1] # self.logger.info('### response referer: ' + response.request.headers.get('Referer', None))
      github_item_loader.add_value('category', category)
      github_item_loader.add_xpath('author', "//body//div[4]//div[1]//div[@id = 'js-repo-pjax-container']//div[1]//h1//span[contains(@class, 'author')]//a//text()")
      github_item_loader.add_xpath('name', "//body//div[4]//div[1]//div[@id = 'js-repo-pjax-container']//div[1]//h1//strong[@itemprop='name']//a//text()")
      github_item_loader.add_xpath('start', "//body//div[4]//div[1]//div[@id = 'js-repo-pjax-container']//div[1]//ul[@class='pagehead-actions']/li[2]//a[@class='social-count js-social-count']//text()")
      github_item_loader.add_xpath('fork', "//body//div[4]//div[1]//div[@id = 'js-repo-pjax-container']//div[1]//ul[@class='pagehead-actions']/li[3]//a[@class='social-count']//text()")
      return github_item_loader.load_item()