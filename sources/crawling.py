import requests
from bs4 import BeautifulSoup
import pandas as pd


def set_data(line):
    data_divide = line.split('/', maxsplit=3)  # 시간 / 이름+내용 분리
    name = data_divide[0]  # 분리된 시간 값을 time 변수에 저장
    time = findtime(name)
    place= findplace(name)  # 장소
    tag = data_divide[3]
    word = [name, place, time, tag]  # 이름-시간-내용에 맞춰서 한 배열로 정리
    return word  # 정리된 형식으로 return


def text_export(text_name):
    place_data = []
    file = open(text_name, 'r', encoding='utf-8-sig')
    lines = file.read().split('\n')
    for line in lines[:-1]:
        data = set_data(line)
        place_data.append(data)

    data = pd.DataFrame(place_data)
    data.columns = ['식당명', '위치', '영업시간', '태그']
    data = data.set_index("식당명")

    data.to_csv('../datas/ADE_place.csv', encoding='euc-kr')


def findplace(search):
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=" + search

    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")

    par_place = soup.findAll("span", attrs={"class": "addr"})
    place = []

    for line in par_place:
        placename = line.get_text()
        place.append(placename)
    return place


def findtime(search):
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=" + search

    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    # par_restaurants = soup.findAll("a", attrs={"class": "biz_name"}
    par_time = soup.findAll("span", attrs={"class": "time"})
    #
    # restaurant_data = []
    # restaurant_data.append(par_restaurants[0].get_text())
    # print(restaurant_data)

    all_time = []
    for line3 in par_time:
        time = line3.get_text()
        all_time.append(time)
    return all_time

def main():
    text_export("../datas/tagdata.txt")

if __name__ == '__main__':
    main()
