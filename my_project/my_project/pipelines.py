# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class MyProjectPipeline:
    def process_item(self, item, spider):
        return item
class ErrorHandlingPipeline:
    def process_item(self, item, spider):
        if 'error' in item:
            error_data = {
                'url': item['url'],
                'error_message': item['error'],
            }
            with open('error_log.json', 'a', encoding='utf-8') as f:
                f.write(json.dumps(error_data, ensure_ascii=False) + '\n')
        return item

class GoogleSearchPipeline:
    def process_item(self, item, spider):
        with open('google_search.json', 'a', encoding='utf-8') as f:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')
        return item

class MySpiderPipeline:
    def process_item(self, item, spider):
        with open('output.json', 'a', encoding='utf-8') as f:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')
        return item