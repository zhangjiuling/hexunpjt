# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from hexunpjt.items import HexunpjtItem
import urllib.request
import urllib.error
import re

class PersonblogSpider(scrapy.Spider):
    name = 'personblog'
    allowed_domains = ['blog.hexun.com']
    uid = '14756002'
    
    def start_requests(self):
        url = 'http://'+self.uid+'.blog.hexun.com/p1/default.html'
        yield Request(url,callback=self.parse,headers={'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Referer':'http://14756002.blog.hexun.com/p2/default.html'})

    def parse(self, response):
        #with open('14756002.html','wb') as htmlfile:
            #htmlfile.write(response.text.encode('utf-8'))
        pages = response.css('.Article')
        js_url = response.css('#DefaultContainer1_ArticleList_Panel1 script::attr(src)').extract_first()
        hitsandcomment = self.get_commnetandhits(js_url,response.url)
        item = HexunpjtItem()
        for page in pages:
            item['title'] = page.css('.ArticleTitleText a::text').extract_first()
            item['link'] = page.css('.ArticleTitleText a::attr(href)').extract_first()
            item['word_count'] = page.css('.ArticleWordCount::text').extract_first()
            hits_comment_id = page.css('.ArticleInfo span::attr(id)').extract() #结果：['click116597112', 'comment116597112']
            item['hits'] = hitsandcomment[hits_comment_id[0]]
            item['comment'] = hitsandcomment[hits_comment_id[1]]
            print(item['hits'],item['comment'])
            yield item
        
        next_page = response.css('.PageSkip .PageSkip_1 a::attr(href)').extract()[-1]
        if next_page:
            print(next_page)
            #print(response.url)
            yield Request(next_page,callback=self.parse,headers={'User-Agent':
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
                        'Referer':response.url})
        
    def get_commnetandhits(self,js_url,referer):
        #以字典的形式返回标签id对应的text，例如：{'click116597112': '1578'}
        id_result = dict()
        req = urllib.request.Request(js_url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0')
        req.add_header('Referer',referer)
        try:
            data = urllib.request.urlopen(req).read()
            data = str(data).replace('"','')
            #print(data)
            results = data.split('$')[2:]
            for result in results:
                temp_list = result.replace('(','').replace(')','').replace(';','').replace("'",'').split(',')
                id_result[temp_list[0]]=temp_list[1]
        except urllib.error.URLError as e:
            if hasattr(e,'code'):
                print(js_url,e.code)
            if hasattr(e,'reason'):
                print(js_url,e.reason)
        #print(id_result)
        return id_result
