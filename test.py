import requests
from bs4 import BeautifulSoup

url = "https://ko.wikipedia.org/wiki/12%EC%9B%94_22%EC%9D%BC"
html_content = requests.get(url).text

soup = BeautifulSoup(html_content, 'html.parser')

# 특정 태그 찾기
start_tag = soup.find('h2', id='사건')
end_tag = soup.find('h2', id='탄생')

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

# 결과 출력
for text in extracted_texts:
    print(text)
