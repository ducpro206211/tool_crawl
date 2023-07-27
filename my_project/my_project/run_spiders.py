from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.exporters import JsonItemExporter

# Import các spider bạn muốn chạy
from my_project.spiders.google_search import GoogleSearchSpider
from my_project.spiders.my_spider import MySpider

# Khởi tạo CrawlerProcess
process = CrawlerProcess(get_project_settings())

# Chạy GoogleSearchSpider để tạo file input.json
process.crawl(GoogleSearchSpider, prompt="mua nhà hà nội")
process.start()

# Load dữ liệu từ file input.json và truyền cho MySpider thông qua `input_file`
with open('google_search.json', 'r', encoding='utf-8') as file:
    data = file.read()
    process.crawl(MySpider, input_file=data)

# Kết thúc quá trình crawl và lưu kết quả vào file output.json
process.settings.set('FEED_FORMAT', 'json')
process.settings.set('FEED_URI', 'output.json')
process.crawl(MySpider, input_file=data)
process.start()
