from sources import manage_file
import pandas as pd

# data file
kakao = "./datas/kakao.txt"
keyword = "./datas/question_keywords.txt"
food = "./datas/food_list.txt"
place = "./datas/place_name.txt"
category = "./datas/category_list.txt"
josa = "./datas/josa_list.txt"
unit_file = "./datas/unit_list.txt"
subway_file = "./datas/subway_station.txt"
except_file = "./datas/except_list.txt"

kakao_log = manage_file.read_file_as_list(kakao)  # 카카오톡 채팅 로그
keyword_dict = manage_file.read_txt_as_dict(keyword)  # 질문 점수
keyword_list = list(keyword_dict.keys())
food_list, food_category_list = [], []  # 음식명
place_list = manage_file.read_file_as_list(place)  # 지역명
category_list = manage_file.read_file_as_list(category)  # 카테고리 대분류 중 식당 목록
josa_list = manage_file.read_file_as_list(josa)  # 조사
unit_list = manage_file.read_file_as_list(unit_file)  # 단위
subway_list = manage_file.read_file_as_list(subway_file)  # 지하철 역명
except_list = manage_file.read_file_as_list(except_file)  # 제외할 단어

place_list.extend(subway_list)

except_list.extend(place_list)
except_list.extend(category_list)
except_list.extend(josa_list)
except_list.extend(unit_list)


def load_food():
    with open(food, 'r', encoding='utf-8') as file:
        tmp_list = file.read().split("-")

        food_list_middle = []
        for word in tmp_list:
            food_list_middle = word.split("\n")
            if food_list_middle[0] == '':
                del food_list_middle[0]
            if food_list_middle[-1] == '':
                del food_list_middle[-1]
            food_category_list.append(food_list_middle)
            food_list.extend(food_list_middle)


load_food()
except_list.extend(food_list)

# result file
already = "./results/already_list.txt"  # 검색기록
restaurant = "./results/restaurant.json"  # 식당 정보
grade = "./results/grade.txt"
match = "./results/match.xlsx"

already_list = manage_file.read_file_as_list(already)
restaurant_dict = manage_file.read_json_as_dict(restaurant)  # 식당 정보
restaurant_list = []


def update():
    restaurant_list.extend(restaurant_dict.keys())


def save_already():
    manage_file.save_list_as_file(already, already_list)


def save_restaurant():
    manage_file.save_dict_as_json(restaurant, restaurant_dict)


def save_grade(score_result):
    with open(grade, 'w', encoding='utf-8') as file:
        for score, sentence, tokens in score_result:
            file.write(str(score) + " : ")
            file.write("{0:100}".format(sentence))
            file.write("// ")
            for token in tokens:
                file.write(token + " ")
            file.write('\n')


def save_match(match_result):
    data = pd.DataFrame(match_result)
    data.columns = ['질문', '답변', '식당']
    data = data.set_index("질문")
    writer = pd.ExcelWriter(match, engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Sheet1')
    writer.save()