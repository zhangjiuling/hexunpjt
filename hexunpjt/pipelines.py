# -*- coding: utf-8 -*-
import codecs
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HexunpjtPipeline(object):
    def open_spider(self,spider):
        self.jsonfile = codecs.open('hexunblog.json','wb',encoding='utf-8')

    def process_item(self, item, spider):
        page = {'title':item['title'],'link':item['link'],'word_count':item['word_count'],
                'hits':item['hits'],'comment':item['comment']}
        line = json.dumps(page,ensure_ascii=False)+'\n'
        self.jsonfile.write(line)
        
        '''
        for i in range(len(item['title'])):
            #title = item['title']
            #link = item['link']
            #word_count = item['word_count']
            #hits = item['hits']
            #comment = item['comment']
            page = {title:item['title'],link:item['link'],word_count:item['word_count'],hits:item['hits'],comment:item['comment']}
            line = json.dumps(page,ensure_ascii=False)+'\n'
            self.jsonfile.write(line)
        '''
        return item

    def close_spider(self,spider):
        self.jsonfile.close()
