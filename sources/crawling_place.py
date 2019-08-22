from twkorean import TwitterKoreanProcessor
import time
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sources import find_tag


def set_data(place_list):
    name = place_list[0]
    if name != '':
        url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=" + name
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")

        time_list = findtime(soup)
        if time_list == []:
            time_list = " "
        find_places_list = findplace(soup)  # 장소
        # tag = data_divide[3]
        time = ', '.join(time_list)
        new_address = place_list[3]
        if len(find_places_list) == 2:
            old_address = find_places_list[1]
        else:
            old_address = " "

        tag = find_tag.tag_list(place_list[2], place_list[1])

        # 카테고리

        word = [name, old_address, new_address,
                time, tag]  # 이름-시간-내용에 맞춰서 한 배열로 정리
        return word  # 정리된 형식으로 return
    else:
        return ''


def text_export(place_lists):
    # [[식당명, 카테고리, 질문+답변 문장, address][][][][]] (날아옴)
    place_data = []
    for place_list in place_lists:
        data = set_data(place_list)
        if data != '':
            if data in place_data: 
                pass
            else:
                place_data.append(data)

    if place_data != []:
        data = pd.DataFrame(place_data)
        data.columns = ['식당명', '지번', '위치', '영업시간', '태그']
        data = data.set_index("식당명")
        dup_remove_data = data.drop_duplicates('위치', keep='first')
        
        writer = pd.ExcelWriter(
            './results/ADE_place.xlsx', engine='xlsxwriter')
        data.to_excel(writer, sheet_name='Sheet1')
        writer.save()


def findplace(soup):
    par_place = soup.findAll("span", attrs={"class": "addr"})
    place = []

    for line in par_place:
        placename = line.get_text()
        place.append(placename)

    return place


def findtime(soup):
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
    # [[식당명, 카테고리, 질문+답변 문장][][][][]] (날아옴)
    # place_list = []
    text_export(place_lists)


if __name__ == '__main__':
    main()
