import re

import scrapy
from scrapy import cmdline

from util.html_header import *
from tiaokan.items import TiaokanItem


class TkSpider(scrapy.Spider):
    item=TiaokanItem()
    name = 'tk'

    def start_requests(self):
        url = ['https://www.tiaokan.me/']

        yield scrapy.Request(url=url[0], callback=self.parse,meta={'i':1,})

        for i in range(2,3):
            url_s=f'https://www.tiaokan.me/page/{i}'
            yield scrapy.Request(url=url_s,callback=self.parse,meta={'i':i,})

    def parse(self, response):
        i=response.meta['i']
        f=open(f'html//home//{i}.html','wb')
        f.write(response.body)

        url_lsit=response.xpath("/html/body/section/div[1]/div/article/header/h2/a/@href").extract()
        print(url_lsit)

        h='''accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: max-age=0
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"
sec-ch-ua-mobile: ?0
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: none
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'''
        c='''wordpress_8074aa8f51c5d6c2cc7c13cf7f0372b2=toby520%7C1620484796%7CQzCma8d5v8zQcyeiWkYY60482frum2TpJoyu4nmcib4%7C325fceeaccb2b6120a8437bb2841d3f0c4fab36d31f8a5d838672bd96cc54b7b; PHPSESSID=7k0ocet2vs3bqb9m2dfphdv09k; wordpress_logged_in_8074aa8f51c5d6c2cc7c13cf7f0372b2=toby520%7C1620484796%7CQzCma8d5v8zQcyeiWkYY60482frum2TpJoyu4nmcib4%7C25b3c3ec1bfa8a50f52fae5b66aba480dd7b51e3c5a1f93b6f17a1ca03c4bd7b;mycred_site_visit=1'''
        hs=headers_sqlit(h)
        # pprint(hs)

        cook = cookies_sqlit(c,'=')
        # pprint(cook)


        for url in url_lsit:

            yield  scrapy.Request(url=url,callback=self.jpg_list,headers=hs,cookies=cook,meta={'hs':hs,'cook':cook})

    def jpg_list(self, response):
        print(response.status)
        # print(response.url.split('/')[-1])
        f=open('html//lsit//'+response.url.split('/')[-1],'wb')
        f.write(response.body)
        print('保存网页html//lsit//'+response.url.split('/')[-1])


        url_id=response.url.split('/')[-1].split('.')[0]
        print(url_id)

        name=response.xpath('/html/body/section/div[1]/div/header/h1/a/text()')[0].extract()
        day=response.xpath('/html/body/section/div[1]/div/header/div/span[1]/text()')[0].extract()
        classify=response.xpath('/html/body/section/div[1]/div/header/div/span[2]/a/text()')[0].extract()
        next_url=response.xpath('//*[@id="erphpdown"]/a/@href')[0].extract()



        item =TiaokanItem()
        item['name']=name
        item['id']=url_id
        item['day']=day
        item['classify']=classify

        print(next_url)
        print(item)

        # pprint(response.meta['hs'])
        # pprint(response.meta['cook'])
        yield scrapy.Request(url=next_url,callback=self.next_url,headers=response.meta['hs'],cookies=response.meta['cook'],meta={'item':item,'hs':response.meta['hs'],'cook':response.meta['cook']})

    def next_url(self,response):
        # print(response.body)
        item = response.meta['item']
        f=open('html/next_url/'+item['id']+'.html','wb')
        f.write(response.body)



        baidu_url=response.xpath('//*[@id="erphpdown-download"]/div/p/a/@href')[0].extract()

        code_data=response.xpath('//*[@id="erphpdown-download"]/div/p/text()')[1].extract()
        # print(code_data)
        code=code_data.split('）')[0].split(':')[-1].split()[0]
        # print(code)


        passwod=response.xpath('//*[@id="erphpdown-download"]/div/div[3]/text()')[0].extract().split('：')[-1]

        baidu_url_data=response.xpath('//*[@id="erphpdown-download"]/div/p/a/@href')[0].extract()
        tiaokan_baidu_url='https://www.tiaokan.me/wp-content/plugins/erphpdown/'+baidu_url_data




        item['code']=code
        item['passwod']=passwod
        item['tiaokan_baidu_url']=tiaokan_baidu_url
        # print(item)

        yield scrapy.Request(url=tiaokan_baidu_url
                             ,headers=response.meta['hs']
                             ,cookies=response.meta['cook']
                             ,meta={'item':item}
                             ,callback=self.baidu)
    def baidu(self,response):
        # f=open('html/5.html','wb')
        # f.write(response.body)
        html = response.text

        baidu_url=re.findall("window.location='(.*?)'",html)
        print(baidu_url[0])


        item = response.meta['item']
        item['baidu_url']=baidu_url[0]
        yield item


        # print(response.body)



if __name__ == '__main__':
    cmdline.execute("scrapy crawl tk  ".split())

