import requests
from bs4 import BeautifulSoup
from sources import find_tag
import re

number = re.compile("[^[0-9]+")

def set_data(place_list):
    name = place_list[0]
    if name != '':
        url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=" + name
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")

        time_list = findtime(soup)
        if time_list == []:
            time_list = " "
        find_places_list = findplace(soup)  # 지번
        time = ', '.join(time_list)
        new_address = place_list[3]  # 도로명
        if len(find_places_list) == 2:
            old_address = find_places_list[1]
        else:
            old_address = " "

        price = findprice(soup)  # 평균 가격

        tag = find_tag.tag_list(place_list[2], place_list[1])

        # 카테고리

        word = [name, old_address, new_address, time, tag]  # 이름-시간-내용에 맞춰서 한 배열로 정리
        return word  # 정리된 형식으로 return
    else:
        return ''


def findplace(soup):
    par_place = soup.findAll("span", attrs={"class": "addr"})
    place = []

    for line in par_place:
        placename = line.get_text()
        place.append(placename)

    return place


def findprice(soup):
    par_price = soup.findAll("em", attrs={"class": "price"})
    prices = []

    for line in par_price:
        price_t = line.get_text()
        price_t = number.sub(" ", price_t)

        try:
            price_t = price_t.split()[0]
            price_t = int(price_t)
            prices.append(price_t)
        except:
            pass

    if prices == []:
        price = 0
    else:
        price = sum(prices) / len(prices)

    return price


def findtime(soup):
    par_time = soup.findAll("span", attrs={"class": "time"})

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
