# -*- coding: utf-8 -*-
import os
from urllib.request import urlretrieve
import logging
import scrapy
from fashion_info.items import FashionInfoItem

start_urls = ["https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo."
                "2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all"
                "&imgfile=&q=%E5%8D%A7%E6%88%BF%E5%AE%B6%E5%85%B7&suggest=history_1&_input_charset="
                "utf-8&wq=&suggest_query=&source=suggest"]
class FinfoSpider(scrapy.Spider):
    name = 'finfo'
    allowed_domains = ["taobao.com"]
    # start_urls = ['http://www.taobao.com/']

    def start_requests(self):
        """
        重写发送请求函数
        :return:
        """
        print("################################################")
        urls = ["https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20180802&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E9%A4%90%E5%8E%85%E5%AE%B6%E5%85%B7&suggest=history_1&_input_charset=utf-8&wq=%E9%A4%90%E5%8E%85&suggest_query=%E9%A4%90%E5%8E%85&source=suggest"]
        for url in urls:
            req = scrapy.Request(url=url,meta={"selenium_url":True},callback=self.parse)
            yield req

    # def parse(self, response):
    #     item = FashionInfoItem()
        # 要爬取的所有男装网址
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # print(response)
        # a_tags = response.xpath('//*[@id="sm-nav-2014"]/div[2]/div[2]/div/div[2]/dl/dd/a')
        # for style_url in style_urls:
        #     new_style_url = quote(style_url,string.printable)
        #     print(new_style_url)
        # print(style_urls)
        # 男装的样式名字
        # style_names = response.xpath('//*[@id="sm-nav-2014"]/div[2]/div[2]/div/div[2]/dl/dd/a/text()').extract()
        # for style_name in style_names:
            # 名字发送到item
            # item["fname"] = style_name

        # 进一步爬取该样式下的所需信息
        # for a_tag in a_tags:
            # 发送二层解析的请求
            # 解析男装样式的名字
            # style_name = a_tag.xpath('.//text()').extract_first()
            # print(style_name)
            # item["fname"] = style_name
            # style_url = quote(a_tag.xpath('.//@href')[0].extract(),string.printable)
            # print(style_url)
            # print(second_url)
            # req = scrapy.http.Request(url=second_url,meta={"item":item,"selenium_url":True},
            #                           callback=self.second_parse,dont_filter=True)
            # if style_url is not None:
            #     yield scrapy.Request(url=style_url,meta={"item":item,"selenium_url":True},callback=self.second_parse)


    # 二层解析
    def parse(self,response):
        # print(response.meta)
        # 接受传过来的item，包含fname
        # print("******************************")
        item = FashionInfoItem()
        # //div[@id="listsrp-itemlist"]/div/div/div[1]/div/div[3]/div[2]/a/text()[2]
        # 找到的60个商品
        clothes = response.xpath('//div[@class="items"]/div')
        # print(clothes)
        item["fname"] = response.xpath('//div[@class="wraper"]/div[2]/div/div/input/@value').extract_first()
        for cloth in clothes:
            print("*************************************")
            content = cloth.xpath('.//div[1]/div[1]/div[1]/a/img/@alt').extract_first().strip()
            # //div[@id="listsrp-itemlist"]/div/div/div[1]/div/div[3]/div[1]/div[1]/strong/text()
            price = cloth.xpath('.//div[2]/div[1]/div[1]/strong/text()').extract_first()
            # 图片名 //div[@id="listsrp-itemlist"]/div/div/div[1]/div/div[1]/div/div[1]/a/img
            img = cloth.xpath('.//div[1]/div[1]/div[1]/a/img/@src').extract_first().replace(" ","")
            full_img = "https:" + img
            print(full_img)
            file_name = "%s.webp"%(content[0:10])
            file_path = os.path.join("/home/gangge/Desktop/practise/spider_prac/day15/"
                                     "fashion_sales/meimei/static/images/canting",file_name)
            print(file_path)
            urlretrieve(full_img,file_path)
            # 销量 //div[@id="listsrp-itemlist"]/div/div/div[1]/div/div[3]/div[1]/div[2]/text()
            sales_str = cloth.xpath('.//div[2]/div[1]/div[2]/text()').extract_first().replace("人付款","")
            sales = int(sales_str)
            # url链接 //div[@id="listsrp-itemlist"]/div/div/div[1]/div/div[3]/div[2]/a/@href
            url = cloth.xpath('.//div[2]/div[2]/a/@href').extract_first()
            # 转到item发到pipelines
            item["content"] = content
            item["price"] = price
            item["img"] = file_name
            item["sales"] = sales
            item["url"] = url
            logging.basicConfig(filename="debug.log",filemode="w",level=logging.DEBUG)
            yield item


