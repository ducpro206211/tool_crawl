import scrapy
from googlesearch import search
# scrapy crawl google_search -o google_search.json

class GoogleSearchSpider(scrapy.Spider):
    name = 'google_search'

    def __init__(self, prompt=None, *args, **kwargs):
        super(GoogleSearchSpider, self).__init__(*args, **kwargs)
        self.prompt = prompt

    def start_requests(self):
        if self.prompt:
            urls = search(self.prompt, num_results=10)
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse, meta={'url': url})

    def parse(self, response):
        yield {
            'url': response.meta['url']
        }
