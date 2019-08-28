import urllib.request
import time
import json
import re
import base64
import sys
import os
from difflib import SequenceMatcher
from sources import datas


검색결과수 = "10"
검색시작위치 = "1"

client_information = [
    ["7Ph92HhYly6BfwHkncbM", "PWciOMPN_p"],  # sehan
    ["6AkDMh30q3LjxKzZC2Oo", "KghRTtlRZu"]  # maylily
]

client_index = 0


def search_local(query):
    # query를 네이버 지도에서 검색
    global client_index

    검색어 = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/local"
    url += "?query=" + 검색어
    url += "&display=" + 검색결과수
    url += "&start=" + 검색시작위치
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_information[client_index][0])
    request.add_header("X-Naver-Client-Secret", client_information[client_index][1])
    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode == 200):
            response_body = response.read()
            time.sleep(0.07)
            return response_body
        else:
            print("Error Code:" + rescode)
            return []
    except Exception as exception:
        print("Exception : " + str(exception))
        print("error query : " + query)
        if client_index < len(client_information) - 1:
            # 대체할 계정이 남은 경우
            client_index += 1
            return search_local(query)
        else:
            # 보유한 계정을 다 사용한 경우
            return -1


def is_restaurant(query, pivot):
    # 검색결과에서 1(검색어와 동일한 식당명), 2(동일 식당명 + a) 찾기

    response_body = search_local(query)  # query를 네이버 지도에서 검색
    if response_body == -1:  # 에러난 경우
        return [], -1

    json_result = json.loads(response_body)  # 검색결과 정리

    results = [[] for _ in range(3)]

    for item in json_result["items"]:
        title = item["title"].replace(" ", "")  # 공백제거한 식당명
        category = item["category"]  # 카테고리 (대분류 > 소분류)
        road_address = item["roadAddress"]  # 도로명
        if category.split('>')[0] in datas.category_list:  # 카테고리 대분류가

            bolds = []  # 검색어와 겹치는 단어들
            lefts = []  # 검색어와 겹치지 않는 단어들
            tmps = title.split("</b>")

            for tmp in tmps[-1].split():
                if tmp != '':
                    lefts.append(tmp)

            for tmp in tmps[:-1]:
                t = tmp.split("<b>")
                if t[0] != '':
                    lefts.append(t[0])
                bolds.append(t[1])

            new_title = ''.join(bolds)
            similar_score = SequenceMatcher(None, pivot, new_title).ratio()
            origin_title = title.replace("<b>", "").replace("</b>", "")

            # 1단계 : query(검색어)와 동일한 title
            if similar_score == 1.0 and len(lefts) == 0:  # 검색어만 있을 때
                results[0].append({"title": origin_title, "category": category, "address": road_address})

            # 2단계 : 동일 title + 다른 단어
            elif similar_score == 1.0 and len(lefts) > 0:
                tmp = ["본점", "본관", "원조", "별관", "분점"]
                t = len(tmp)
                for left in lefts:
                    if left in tmp:
                        t = tmp.index(left)
                        break
                results[1].append([{"title": origin_title, "category": category, "address": road_address}, t])

            # 3단계 : 유사 title
            else:
                results[2].append([{"title": origin_title, "category": category, "address": road_address}, similar_score])

    results[1].sort(key=lambda x: x[1])
    for i in range(len(results[1])):
        results[1][i] = results[1][i][0]

    results[2].sort(key=lambda x: x[1], reverse=True)
    for i in range(len(results[2])):
        results[2][i] = results[2][i][0]

    check = 3

    if len(results[0]) + len(results[1]) + len(results[2]) == 0:  # 없음
        check = 0
    elif len(results[0]) + len(results[1]) == 0:  # 3순위
        check = 1
        if query != pivot:
            check = 3
    elif len(results[0]) == 0:  # 2, 3순위
        check = 2

    return results, check


def check_name(query, pivot):
    # 네이버 지도 검색해서 1순위 or 2순위 있으면 return
    results, check = is_restaurant(query, pivot)  # 검색결과에서 1(검색어와 동일한 식당명), 2(동일 식당명 + a) 찾기
    if check == -1:
        # 에러가 발생한 경우 : api 1일 할당량 초과
        return -1
    elif check == 0:
        # 검색 결과 없는 경우 : 식당 이름이 아니라고 추측
        return []
    elif check == 1:
        # 유사 결과만 있는 경우
        return []
    elif check == 2:
        # 식당 이름인 경우 (1순위 없이 2순위만 있는 경우)
        return results
        # return []
    elif check == 3:
        # 식당 이름인 경우
        return results
    else:
        # 알 수 없는 경우
        print("비정상 check 발견")
        return -1
