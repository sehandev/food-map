# -*- coding: utf-8 -*-

import urllib.request
import time
import json
import re
import base64
from difflib import SequenceMatcher

from find_name import kakao_log_to_nouns

with open("/home/sehan/git/food-map/datas/category_list.txt", 'r') as file:
    categories = file.read().split('\n')

except_file = "/home/sehan/git/food-map/datas/except_list.txt"
excepts = set()

검색결과수 = "30"
검색시작위치 = "1"

# sehan
# client_id = "7Ph92HhYly6BfwHkncbM"
# client_secret = "PWciOMPN_p"

# maylily
clinet_id = "6AkDMh30q3LjxKzZC2Oo"
client_secret = "KghRTtlRZu"


def search_local(query):
    검색어 = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/local"
    url += "?query=" + 검색어
    url += "&display=" + 검색결과수
    url += "&start=" + 검색시작위치
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode == 200):
            response_body = response.read()
            time.sleep(0.04)
            # print(response_body.decode('utf-8'))
            return response_body
        else:
            print("Error Code:" + rescode)
    except:
        print("error : " + query)
        return False


def print_result(count, results, index):
    length = len(results[index])
    if length == 0:
        # print(str(index + 1) + "순위 결과 없음")
        pass
    elif count - length > 0:
        print(str(index + 1) + "순위")
        print(*results[index], sep="\n")
        count -= length
    else:
        print(str(index + 1) + "순위")
        print(*results[index][:count], sep="\n")

    return count


def is_rastaurant(query):
    respons_body = search_local(query)
    if not respons_body:  # 에러난 경우
        return "", [], -1

    json_result = json.loads(respons_body)

    results = [[] for _ in range(3)]

    for item in json_result["items"]:
        title = item["title"]
        category = item["category"]
        roadAddress = item["roadAddress"]
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
                results[0].append({"title": origin_title, "category": category, "address": item["roadAddress"]})

            # 2단계 : 동일 title + 다른 단어
            elif similar_score == 1.0 and len(lefts) > 0:

                tmp = ["본점", "본관", "원조", "별관", "분점"]
                t = len(tmp)
                for left in lefts:
                    if left in tmp:
                        t = tmp.index(left)
                # results[1].append([{"title": origin_title, "category": category, "address": item["roadAddress"]}, t])

            # 3단계 : 유사 title
            else:
                # results[2].append([{"title": origin_title, "category": category, "address": item["roadAddress"]}, similar_score])
                pass

    results[1].sort(key=lambda x: x[1])
    for i in range(len(results[1])):
        results[1][i] = results[1][i][0]

    # results[2].sort(key=lambda x: x[1], reverse=True)
    # for i in range(len(results[2])):
    #     results[2][i] = results[2][i][0]

    check = 2

    if len(results[0]) + len(results[1]) + len(results[2]) == 0:
        check = 0
    elif len(results[0]) + len(results[1]) == 0:
        check = 1

    return roadAddress, results, check


def check_name(query):
    address, results, check = is_rastaurant(query)
    if check == -1:
        pass
    elif check == 0:
        pass
        # print("식당 이름이 아님")
    elif check == 1:
        pass
        # print("유사 결과만 있음")
        # print_result(5, results, i)
    elif check == 2:
        print(query + " / " + address)
    # print('='*20)


if __name__ == "__main__":
    with open("../datas/kakao_processed_only_log.txt", 'r') as file:
        sentences = file.read().split('\n')
        for sentence in sentences:
            # print("카톡 내용 : " + sentence)
            names = kakao_log_to_nouns(sentence)
            for name in names:
                if len(name) > 2:
                    check_name(name)
    with open(except_file, 'w') as file:
        for ex in excepts:
            file.write(ex + '\n')
