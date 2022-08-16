import requests
from bs4 import BeautifulSoup
import re

# requests 작업과 soup 객체 만드는 함수 정의


def create_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup


def print_news(index, title, link):
    print("{}. {}".format(index+1, title))
    print(f'  (링크 : {link})')


def Today_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    cast = soup.find("p", attrs={"class": "summary"}).get_text()
    cur_temp = (
        soup.find("div", attrs={"class": "temperature_text"})
        .get_text()
        .replace("온도", "온도 ").strip()
    )
    min_temp = (
        soup.find("span", attrs={"class": "lowest"}
                  ).get_text().replace("기온", "기온 ")
    )
    max_temp = (
        soup.find("span", attrs={"class": "highest"}
                  ).get_text().replace("기온", "기온 ")
    )

    rain_rates = soup.find(
        "div", attrs={"class": "cell_weather"}).get_text().replace("  ", " ").strip()

    Today_etc = soup.find(
        "ul", attrs={"class": "today_chart_list"}).get_text().replace("  ", " ").strip()

    # 출력
    print(cast)
    print(f'{cur_temp} ({min_temp} / {max_temp})')
    print(f'강수확률 : {rain_rates}')
    print(Today_etc)
    print()


def sports_news():
    print("[헤드라인 뉴스]")
    url = "https://sports.news.naver.com/wfootball/index"
    soup = create_soup(url)
    news_list = soup.find(
        "ol", attrs={"class": "news_list"}).find_all("li", limit=3)  # 3개로 제한
    for index, news in enumerate(news_list):
        title = news.find("a").get_text().strip()
        link = "https://sports.news.naver.com/" + news.find("a")["href"]
        print_news(index, title, link)
        print()


def IT_news():
    print("[IT 뉴스]")
    url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    news_list = soup.find(
        "ul", attrs={"class": "type06_headline"}).find_all("li", limit=3)
    for index, news in enumerate(news_list):
        # 기사의 이미지 존재에 따라 가져와야 하는 a태그가 달라지므로 if문을 이용

        a_idx = 0
        img = news.find("img")
        if img:
            a_idx = 1  # img 태그가 있으면 1번째 a태그의 정보를 사용

        title = news.find_all("a")[a_idx].get_text().strip()
        link = news.find_all("a")[a_idx]["href"]
        print_news(index, title, link)
        print()


def Today_english():
    print("[오늘의 영어 회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
    soup = create_soup(url)
    # 정규식을 사용하여 conv_kor_t 로 시작하는 id를 조회
    sentences = soup.find_all("div", attrs={"id": re.compile("^conv_kor_t")})
    print("(영어 지문)")
    # conv_kor_t 로 시작하는 id가 n개 조회될 시 앞의 n/2개는 한글지문, 뒤의 n/2개는 영어지문이므로 슬라이싱을 이용하여 영어지문 먼저 출력
    for sentence in sentences[len(sentences)//2:]:
        print(sentence.get_text().strip())

    print("\n(한글 지문)")
    for sentence in sentences[:len(sentences)//2]:
        print(sentence.get_text().strip())


if __name__ == "__main__":
    Today_weather()  # 오늘의 날씨 정보
    sports_news()  # 스포츠 뉴스 정보
    IT_news()  # IT 뉴스 정보
    Today_english()
