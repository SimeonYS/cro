import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import CroItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class CroSpider(scrapy.Spider):
	name = 'cro'
	start_urls = ['https://www.sberbank.hr/o-nama/press-portal/']

	def parse(self, response):
		post_links = response.xpath('//div[@id="announcementsForMedia"]//td/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):

		date = response.xpath('//div[@class="art-head"]/p/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="art-body"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=CroItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
