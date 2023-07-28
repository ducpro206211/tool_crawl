import scrapy
from bs4 import BeautifulSoup
import json
import os
import re  # Thêm thư viện re để sử dụng biểu thức chính quy

class MySpider(scrapy.Spider):
    name = 'my_spider'
    def start_requests(self):
        # Replace 'google_search.json' with the output file from the GoogleSearchSpider
        with open(os.getcwd()+'/my_project/google_search.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for entry in data:
            url = entry['url']
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        content = []

        # ... Các bước xử lý và trích xuất dữ liệu từ BeautifulSoup như trong đoạn mã trước ...
        # Lấy tiêu đề h1
        h1_tags = soup.select('h1')
        for h1_tag in h1_tags:
            cleaned_text = self.clean_text(h1_tag.get_text())  # Loại bỏ biểu thức chính quy
            content.append(cleaned_text)

        # Lấy tiêu đề h2
        h2_tags = soup.select('h2')
        for h2_tag in h2_tags:
            cleaned_text = self.clean_text(h2_tag.get_text())  # Loại bỏ biểu thức chính quy
            content.append(cleaned_text)

        # Lấy nội dung các thẻ p mà không chứa thẻ a
        p_tags = soup.select('p:not(:has(a))')
        for p_tag in p_tags:
            cleaned_text = self.clean_text(p_tag.get_text())  # Loại bỏ biểu thức chính quy
            content.append(cleaned_text)

        # Tạo kết quả thành JSON
        result = {
            'url': response.url,
            'content': content
        }

        # Lưu kết quả vào tệp JSON
        with open('output.json', 'a', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False)
            f.write('\n')

    def clean_text(self, text):
        # Sử dụng biểu thức chính quy để loại bỏ các ký tự không mong muốn
        cleaned_text = re.sub(r'[\t\n\r]', ' ', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        cleaned_text = cleaned_text.strip()
        return cleaned_text
