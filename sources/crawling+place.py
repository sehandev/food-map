from twkorean import TwitterKoreanProcessor
import time
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def set_data(line):
    data_divide = line.split('/', maxsplit=3)  # 시간 / 이름+내용 분리
    name = data_divide[0]  # 분리된 시간 값을 time 변수에 저장
    time = findtime(name)
    place = findplace(name)  # 장소
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

    data.to_csv('ADE_place.csv', encoding='euc-kr')


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
    text_export("tagdata.txt")

    names = kakao_log_to_nouns("백화양곱창도 좋아요!")
    print(names)



processor = TwitterKoreanProcessor(normalization=False, stemming=False)
hangul = re.compile("[^ 0-9가-힣]+")


def kakao_log_to_nouns(sentence):

    names = set()  # 찾은 이름을 저장할 set
    line = hangul.sub(" ", sentence)

    # 1단계 : 띄어쓰기 기준
    words = line.split()
    for word in words:
        tmp = hangul.sub(" ", word).split()
        for word in tmp:
            names.add(word)

    # 2단계 : 명사 기준
    # example : [KoreanToken(text='준비된', pos='Verb', unknown=False), ... ]
    tokens = processor.tokenize(line)

    for token in tokens:
        if token[1] == "Noun":
            names.add(token[0])

    # 3단계 : 조사 기준
    for word in words:
        tokens = processor.tokenize(word)

        tmp = ""
        for token in tokens:
            if token[1] != "Josa":
                tmp += token[0]

        names.add(tmp)

    return list(names)



if __name__ == '__main__':
    main()
