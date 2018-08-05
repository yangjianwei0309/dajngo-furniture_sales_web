# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class FashionInfoPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(user="root",
                                       password="842655",
                                       db="project",
                                       host="127.0.0.1",
                                       port=3306,
                                       charset="utf8")
        self. cursor = self.connect.cursor()

    def process_item(self, item, spider):
        fname = item["fname"]
        content = item["content"]
        price = item["price"]
        img = item["img"]
        sales = item["sales"]
        url = item["url"]
        sql = "insert into furniture(fname,content,price,img,sales,url) values(%s,%s,%s,%s,%s,%s);"
        # 执行sql语句，向数据库插入数据
        self.cursor.execute(sql,(fname,content,price,img,sales,url))
        self.connect.commit()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()
