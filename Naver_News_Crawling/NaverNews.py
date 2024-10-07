import requests
from bs4 import BeautifulSoup
import csv

# 카테고리별 URL
categories = {
    '모바일': 'https://news.naver.com/breakingnews/section/105/731',
    '인터넷/SNS': 'https://news.naver.com/breakingnews/section/105/226',
    '통신/뉴미디어': 'https://news.naver.com/breakingnews/section/105/227',
    'IT일반': 'https://news.naver.com/breakingnews/section/105/230',
    '보안/해킹':'https://news.naver.com/breakingnews/section/105/732',
    '컴퓨터':'https://news.naver.com/breakingnews/section/105/283',
    '게임/리뷰':'https://news.naver.com/breakingnews/section/105/229',
    '과학 일반':'https://news.naver.com/breakingnews/section/105/228'
}

def get_news_from_category(category_url):
    data = []
    
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 뉴스 리스트 추출
    news_list = soup.find_all('div', class_='sa_text')

    for news in news_list[:30]:  # 첫 30개만 추출
        #제목 추출
        title = news.find('strong', class_='sa_text_strong').get_text().strip()
        #링크 추출
        link = news.find('a')['href']  #<a> 태그에서.
        # 언론사 추출
        press = news.find('div', class_='sa_text_press').get_text().strip()
        # 내용 추출
        content = news.find('div', class_='sa_text_lede').get_text().strip()
        
        data.append([press, title, link, content])  # 언론사, 타이틀, 링크, 내용 저장
    
    return data

# 모든 카테고리 수집 및 출력
all_data = []
for category, url in categories.items():
    print(f"{category} 뉴스")  # 카테고리명 출력
    print("-" * 50)
    
    # 해당 카테고리 뉴스 수집
    news_data = get_news_from_category(url)
    
    # 수집된 뉴스 미리보기
    for idx, news in enumerate(news_data):
        print(f"{idx+1}. Press: {news[0]}")
        print(f"   Title: {news[1]}")
        print(f"   Link: {news[2]}")
        print(f"   Content: {news[3]}")
        print("-" * 50)
    
    for news in news_data:
        all_data.append([category] + news)  # 카테고리+언론사+제목+링크+내용을 저장(csv 저장 위해)

# CSV로 저장
with open('final_naver_it_science_news.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Category', 'Press', 'Title', 'Link', 'Content'])  # 헤더 추가
    writer.writerows(all_data)

print('Data collection completed.')
