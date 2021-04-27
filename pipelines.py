# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


class TiaokanPipeline:
    def process_item(self, item, spider):
        db = pymysql.connect("localhost", "testuser", "test123", "TESTDB")

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT VERSION()")

        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchone()

        print("Database version : %s " % data)

        return item
