import os
import json
from flask_cors import CORS
from flask import (
    Flask,
    make_response,
    jsonify,
    request,
    send_file,
    send_from_directory,
    abort,
)
app = Flask(__name__)
CORS(app)
def run_spiders(prompt):
    # Đường dẫn đến thư mục chứa project Scrapy của bạn
    scrapy_project_path = "my_project"

    # Thay đổi thư mục làm việc hiện tại đến thư mục chứa project Scrapy
    os.chdir(scrapy_project_path)
    # Xoá dữ liệu trong file "google_search.json" và "output.json" trước khi chạy lại spider với prompt mới
    with open('google_search.json', 'w') as f:
        f.write('')
    with open('output.json', 'w') as f:
        f.write('')
    # Thực thi Spider "GoogleSearchSpider" với prompt như đầu vào
    google_search_cmd = f'scrapy crawl google_search -a prompt="{prompt}" -o google_search.json'
    os.system(google_search_cmd)

    # Thực thi Spider "MySpider" với input_file là "google_search.json"
    my_spider_cmd = 'scrapy crawl my_spider -a input_file=google_search.json -o output.json'
    os.system(my_spider_cmd)
def load_json_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]
@app.route('/api/search', methods=['POST'])
def search_and_return_result():
    try:
        # Nhận đầu vào dạng JSON từ client
        data = request.get_json()

        # Lấy nội dung của trường "prompt" từ JSON
        prompt = data.get('prompt', '')

        if prompt:
            # Chạy hàm run_spiders với prompt nhận được
            run_spiders(prompt)

            # Đọc dữ liệu từ file output.json
            output_data = load_json_from_file('output.json')

            return jsonify(output_data)

        else:
            return jsonify({'error': 'Missing or invalid "prompt" field in JSON.'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9000)
