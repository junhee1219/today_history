import json
import os
import re
import google.generativeai as genai
from flask import Flask, jsonify, request, send_file, send_from_directory
import requests
from bs4 import BeautifulSoup


def get_wiki_data (UTCMap):
    #12월_22일
    url = f"""https://ko.wikipedia.org/wiki/{UTCMap["month"]}%EC%9B%94_{UTCMap["day"]}%EC%9D%BC"""
    print(url)
    html_content = requests.get(url).text
    print(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')

    # 특정 태그 찾기
    start_tag = soup.find( id='사건')
    end_tag = soup.find( id='탄생')

    # 시작 태그와 종료 태그 사이의 내용 추출
    content_between_tags = []
    current_element = start_tag.find_next()
    while current_element and current_element != end_tag:
        content_between_tags.append(str(current_element))
        current_element = current_element.find_next()

    # 추출한 내용을 다시 BeautifulSoup 객체로 변환
    soup_between_tags = BeautifulSoup(''.join(content_between_tags), 'html.parser')

    # 모든 <li> 태그를 찾음
    list_items = soup_between_tags.find_all('li')

    # 텍스트를 추출하는 함수
    def extract_text(item):
        # 각 <a> 태그의 텍스트를 추출
        for a in item.find_all('a'):
            # 링크 텍스트를 변환
            a.replace_with(a.text)
        return item.get_text()

    # 각 <li> 태그에서 텍스트를 추출
    extracted_texts = [extract_text(item) for item in list_items]
    result = ""
    # 결과 출력
    for text in extracted_texts:
        result = text + "\n"
    print(result)
    return result


API_KEY = 'AIzaSyDOmX_rexV3rmoigVsCbypYNycZS5MyV7E'

genai.configure(api_key=API_KEY)

def extract_json_from_text(text):
    text = text.replace("'",'"')
    print(text)
    try:
        print("this1")
        return json.loads(text)
    except :
        # 정규 표현식을 사용하여 ```로 둘러싸인 부분을 찾기
        regex = r'```json([\s\S]*?)```'
        matches = re.findall(regex, text)

        # 첫 번째 JSON 블록을 파싱하여 객체로 변환
        if matches:
            try:
                json_object = json.loads(matches[0])
                print("this2")
                return json_object
            except json.JSONDecodeError as error:
                print('JSON 파싱 오류:', error)
                return []
        else:
            print('JSON 블록을 찾을 수 없음')
            return []
    
    
def get_main_prompt(UTCMap):
       
    return f"""
###{UTCMap["month"]}월 {UTCMap["day"]}일에 일어났던 역사적 사건들(위키피디아 참고)
{get_wiki_data (UTCMap)}
    ###오늘의 역사 라는 서비스를 할거야. 상상력을 조금 포함해서(단, 근거는 있어야 함) "현재 무슨일이 일어나고 있다"와 같은 형태로 현장에 있는것처럼 묘사해서 두줄로 써줘.
    타임머신을 타고 과거여행을 하는 것이라고 생각하면 돼. 말투는 이모지를 포함한 구어체로 써줘. 위에 위키피디아 자료가 이상하거나 부실하면 니가 알고있는 지식을 추가해도 돼.

###{UTCMap["year"]}년을 제외한 년도 중 {UTCMap["month"]}월 {UTCMap["day"]}일 {UTCMap["hour"]}시 {UTCMap["minute"]}분에 일어났을 역사적인 사건을 묘사해줘.
시간 기준으로 아직 일어나지 않았을 것 같은 일은 절대 쓰면 안돼. 

###다음 json 형태에 맞춰 년도기준 내림차순으로 중요한 사건 위주로 최대 20개까지만 써줘. 
{
	[
		{"year" : "1592" , "content" : "내용"}
		, ...
	]
}
"""

app = Flask(__name__)

@app.route("/")
def index():
    return send_file('web/index.html')

@app.route("/web/<path:path>")
def serve_static(path):
    return send_from_directory('web', path)

@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        try:
            req_body = request.get_json()
            print(request)
            content = get_main_prompt(req_body["CurMap"])
            model = genai.GenerativeModel(model_name='gemini-1.5-pro')
            response = model.generate_content(content)
            json_text = extract_json_from_text(response.text)
            print(response)
            if json_text == []:
                response = model.generate_content(content)
                json_text = extract_json_from_text(response.text)
            if json_text == []:
                return [{"year":"2024" ,"content": "사용량이 너무 많아! 새로고침 부탁해😢"}]
            return json_text
        except Exception as e:
            return jsonify({ "error": str(e) })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
