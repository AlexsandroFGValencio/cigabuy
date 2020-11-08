# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.cigabuy.com']
    start_urls = ['http://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html']

    def parse(self, response):
        products = response.xpath("//div[@class='r_b_c']/div[@class='p_box_wrapper']/div")
        for product in products:
            product_name = product.xpath(".//a[@class='p_box_title']/text()").get()
            product_link = response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get())
            original_product_price = product.xpath(".//div[@class='p_box_price cf']/span[@class='normalprice fl']/text()").get()
            discountned_product_price = product.xpath(".//div[@class='p_box_price cf']/span[@class='productSpecialPrice fl']/text()").get()

            yield {
                'product_name': product_name,
                'product_link': product_link,
                'original_product_price': original_product_price,
                'discountned_product_price': discountned_product_price
            }

            next_page = response.xpath("(//a[@class='nextPage']/@href)[position()=1]").get()
            
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)

