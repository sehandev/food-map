from twkorean import TwitterKoreanProcessor
import time
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from find_name import kakao_log_to_nouns


def set_data(name):
    name = findname(name)  # 분리된 시간 값을 time 변수에 저장
    if name != '':
        time_list = findtime(name)
        place_list = findplace(name)  # 장소
        # tag = data_divide[3]
        time = ', '.join(time_list)

        new_address = place_list[0]
        old_address = place_list[1]
        
        # 카테고리

        word = [name, old_address, new_address, time]  # 이름-시간-내용에 맞춰서 한 배열로 정리
        print("word: "+str(word))
        return word  # 정리된 형식으로 return
    else:
        return ''


def text_export(names):
    place_data = []
    for name in names:
        data = set_data(name)
        if data != '':
            place_data.append(data)

    if place_data != []:
        data = pd.DataFrame(place_data)
        data.columns = ['식당명', '지번', '위치', '영업시간']
        data = data.set_index("식당명")

        data.to_csv('../datas/ADE_place.csv', encoding='euc-kr')

def findname(search):
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=" + search
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    par_restaurants = soup.findAll("a", attrs={"class": "biz_name"})

    for line in par_restaurants:
        name =  line.get_text()
        return name
    return ''

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
    names = kakao_log_to_nouns("호호미욜도 좋아요!")
    print(names)
    text_export(names)

if __name__ == '__main__':
    main()
