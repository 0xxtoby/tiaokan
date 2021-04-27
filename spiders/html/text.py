s='提取码: wz40）'
print(s.split('）')[0].split(':')[-1].split(':')[-1])


sql={'baidu_url': ['https://pan.baidu.com/s/1huJVw0-TYuMi28q_SWq2sw'],
 'classify': '老司机',
 'code': 'wz40',
 'day': '2021-04-25',
 'id': '62099',
 'name': '天美传媒 英雄救美 563M',
 'passwod': 'tiaokan.vip',
 'tiaokan_baidu_url': 'https://www.tiaokan.me/wp-content/plugins/erphpdown/download.php?postid=62099&key=1'}

import pymysql


#连接数据库

try:
    db = pymysql.connect(host="localhost", user="root", password="tjx158589", database="tiaokan2",charset="utf8")
    print("数据库连接成功")
except pymysql.Error as e:
    print("数据库连接失败："+str(e))


#使用cursor()方法创建一个游标对象
cursor = db.cursor()

sql = f"""INSERT INTO baidu_data
         VALUES ('{sql['id']}'
,'{sql['name']}'
,'{sql['day']}'
,'{sql['baidu_url'][0]}'
,'{sql['code']}'
,'{sql['passwod']}'
,'{sql['classify']}'
,'{sql['tiaokan_baidu_url']}'

)"""




print(sql)
try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
   print('tianjiaceng')
except:
   # 如果发生错误则回滚
   db.rollback()
   print('cuowu')



#使用execute()方法执行SQL语句
cursor.execute("SELECT * FROM baidu_data")

#使用fetall()获取全部数据
data = cursor.fetchall()

#打印获取到的数据
print(data)

#关闭游标和数据库的连接
cursor.close()
db.close()


