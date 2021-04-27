# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TiaokanItem(scrapy.Item):
    # define the fields for your item here like:
    # 页面名字
    name = scrapy.Field()
    # 更新时间
    day = scrapy.Field()
    # 分类
    classify= scrapy.Field()
    tiaokan_baidu_url= scrapy.Field()
    #百度云连接
    baidu_url = scrapy.Field()
    #提取码
    code = scrapy.Field()
    # 解压密码
    passwod = scrapy.Field()

    id = scrapy.Field()


    pass
