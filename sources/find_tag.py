import re

range_1 = [5,6,7,8,9] #4-10만원 중간의 범위
range_2 = [11,12,13,14,15,16,17,18,19] # 10~20만원 중간의 범위
# 숫자~숫자+만원, 숫자+만원
# 숫자~숫자+만, 숫자+만
# 숫자에 따라서 1만원 미만, 1~2만원대, 2~4만원대, 4~10만원대, 10~20만원대, 20만원 이상으로 나누어 return한다
# 문자열로 return됨

# 음식종류 - 질문의 경우 find_inform, 대답의 경우 음식점 정보에서 가져오면 됨

def tag_list(sentence, kind_of_food):
    tag_data = []
    price = is_it_money(sentence)
    tag_data.append("#" + price)  #tag에 가격 추가
    tag_data.append("#" + kind_of_food)  #tag에 음식 카테고리 추가

    # 하위 : 부가적인 태그들 추가
    if "가성비" in sentence :
        tag_data.append("#가성비_좋은")
    if "파인다이닝" in sentence :
        tag_data.append("#파인다이닝")
    if "분위기" in sentence :
        tag_data.append("#분위기_좋은")
    if "데이트" in sentence :
        tag_data.append("#데이트")

    # list형태로 정렬된 tag를 일련의 목록으로 만드는 과정
    tag = str(tag_data[0])  # 첫번째 태그
    for i in range(0, len(tag_data)-1):
        tag = tag + " " + str(tag_data[i+1])  #첫번째 태그에 뒤따른 태그들 잇는 for문
    return tag

# 질문, 대답에 있으면 연결
# 가성비 -> 가성비좋은
# 분위기 -> 분위기 좋은
# (질문) 파인다이닝-> 파인다이닝

# 영업시간 -> 이미 가져왔음
# 지역 -> 이미 나옴

def is_it_money(sentence):
    one_number = re.compile("[0-9]만원")
    one_number_match = one_number.findall(sentence)

    two_number = re.compile("[0-9]~[0-9]만원")
    two_number_match = two_number.findall(sentence)

    two_number_space = re.compile("[0-9]~[0-9]\s만원")
    two_number_space_match = two_number_space.findall(sentence)

    if two_number_space_match != []:
        price = price_tag(str(two_number_space_match))
        return price
    elif two_number_match != "":
        price = price_tag(str(two_number_match))
        return price
    elif one_number_match != "":
        price = price_tag(str(one_number_match))
        return price
    else : return


def price_tag(sentence):
    price_tag_range = []
    price_tag_data = []
    number = re.compile("[0-9]")
    number_match = number.findall(sentence)

    boundary = [2,4,10,20]

    for i in range(0, len(number_match)):
        num = int(number_match[i])
        if num in boundary:
            price_tag_range.append(num)  # 만일 boundary값일 경우 값 추가
        if num == 1 :  # [1만원대]라고 언급했을 경우 1~2만원대에 추가
            price_tag_range = [1,2]
        elif num == 3 : # [3만원대] 라고 언급했을 경우 2~4만원대에 추가
            price_tag_range = [2,3,4]
        elif num in range_1 : # num이 5~9 내에 있을 경우 4~10만원대 추가
            price_tag_range = [4,5,6,7,8,9,10]
        elif num in range_2 : # num이 10~19에 있을 경우 10~20만원대 추가
            price_tag_range = [10,11,12,13,14,15,16,17,18,19,20]
        elif num > 20 :  # 20 이상 시 "20만원 이상"
            price_range = "20만원_이상"
            return price_range

    price_tag_range = list(set(price_tag_range))  # boundary값과 설정된 price_tag_range가 중복될 경우 중복제거
    if len(price_tag_range) == 0:
        price_range = "가격정보_없음"
    elif price_tag_range == 1:
        price_range = str(price_tag_range[0]) + "만원대"
    else : price_range = str(price_tag_range[0]) + "~" + str(price_tag_range[-1]) + "만원"
    return price_range

if __name__ == "__main__" :
    tag_list(sentence, kind_of_food)