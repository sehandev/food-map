import urllib.request
import time
import json
import re
import base64
import sys
import os
from difflib import SequenceMatcher
from sources import manage_file

categories = manage_file.read_file_as_list("./datas/category_list.txt")

검색결과수 = "10"
검색시작위치 = "1"

client_information = [
    ["7Ph92HhYly6BfwHkncbM", "PWciOMPN_p"],  # sehan
    ["6AkDMh30q3LjxKzZC2Oo", "KghRTtlRZu"]  # maylily
]

client_index = 0


def search_local(query):
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
            time.sleep(0.05)
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


def is_rastaurant(query):
    response_body = search_local(query)
    if response_body == -1:  # 에러난 경우
        return [], -1

    json_result = json.loads(response_body)

    results = [[] for _ in range(3)]

    for item in json_result["items"]:
        title = item["title"]
        category = item["category"]
        road_address = item["roadAddress"]
        if category.split('>')[0] in categories:

            bolds = []  # 검색어에 겹치는 단어들
            lefts = []  # 검색어에 겹치지 않는 단어들
            tmps = title.split("</b>")

            for tmp in tmps[-1].split():
                if tmp != '':
                    lefts.append(tmp)

            for tmp in tmps[:-1]:
                t = tmp.split("<b>")
                if t[0] != '':
                    lefts.append(t[0])
                bolds.append(t[1])

            new_title = ' '.join(bolds)
            similar_score = SequenceMatcher(None, query, new_title).ratio()
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

    if len(results[0]) + len(results[1]) + len(results[2]) == 0:
        check = 0
    elif len(results[0]) + len(results[1]) == 0:
        check = 1
    elif len(results[0]) == 0:
        check = 2

    return results, check


def print_result(count, results, index):
    length = len(results[index])
    if length == 0:
        print(str(index + 1) + "순위 결과 없음")
        pass
    elif count - length > 0:
        print(str(index + 1) + "순위")
        print(*results[index], sep="\n")
        count -= length
    else:
        print(str(index + 1) + "순위")
        print(*results[index][:count], sep="\n")

    return count


def check_name(query):
    results, check = is_rastaurant(query)
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
        # return results
        return []
    elif check == 3:
        # 식당 이름인 경우
        return results

        # 1순위, 2순위, 3순위 출력
        # count = 6
        # for i in range(3):
        #     count = print_result(count, results, i)
    else:
        # 알 수 없는 경우
        print("비정상 check 발견")
        return -1
