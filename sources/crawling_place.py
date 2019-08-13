from twkorean import TwitterKoreanProcessor
import time
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from find_tag import tag_list

def set_data(name, place_list, i):
    # [[식당명, 카테고리, 질문+답변 문장][][][][]] (날아옴)
    if name != '':
        time_list = findtime(name)
        print(time_list)
        places_list = findplace(name)  # 장소
        # tag = data_divide[3]
        time = ', '.join(time_list)
        new_address = places_list[0]
        old_address = places_list[1]

        tag = tag_list(place_list[2], place_list[1])
        # 카테고리

        word = [name, old_address, new_address, time, tag]  # 이름-시간-내용에 맞춰서 한 배열로 정리
        print("word: "+str(word))
        return word  # 정리된 형식으로 return
    else:
        return ''


def text_export(place_list):
    names = []
    for i in range(0, len(place_list)):
        names.append(place_list[i][0])
    print(names)
    place_data = []
    for name in names:
        print(name)
        i = names.index(name)
        data = set_data(name, place_list[i], i)
        if data != '':
            place_data.append(data)

    if place_data != []:
        data = pd.DataFrame(place_data)
        data.columns = ['식당명', '지번', '위치', '영업시간', '태그']
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
    #[[식당명, 카테고리, 질문+답변 문장][][][][]] (날아옴)
    # place_list = []
    place_list = []
    place_list = [["해우리참치", "한식", "혹시 공덕에 가성비 4~6만원 이하 회식장소 있나요? 해우리도 좋아요"],["호호미욜","카페", "홍대에 분위기 좋은 카페 있나요? 호호미욜 좋아요"]]
    text_export(place_list)

if __name__ == '__main__':
    main()
