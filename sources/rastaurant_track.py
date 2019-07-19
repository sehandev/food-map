import json

import naver_local
import kakao_noun


found_nouns = kakao_noun.kakao_log_to_nouns("./kakao.txt")
# found_nouns example : {'옥토버', '채팅', '종류', '와글와글', ... , '남면', '섭취', '장탕'}

with open("./category_list.txt", 'r') as file:
    categories = file.read().split('\n')[:-1]

for noun in found_nouns:
    if len(noun) > 1:
        local_result = naver_local.search_local(noun)
        json_result = json.loads(local_result)
        for item in json_result["items"]:
            if item["category"] in categories:
                print("검색어 : " + noun)
                print("가게 이름 : " + item["title"].replace("<b>", "").replace("</b>", "").replace("&amp;", "&"))
                print("카테고리 : " + item["category"].replace(">", " > "))
                if item["roadAddress"]:
                    print("주소 : " + item["roadAddress"])
                print()
                break
