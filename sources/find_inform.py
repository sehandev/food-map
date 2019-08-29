from sources import datas


def food_category(food_name):
    for j in range(0, 8):
        for k in range(0, len(datas.food_category_list[j])):
            if food_name == datas.food_category_list[j][k]:
                food_category = datas.food_category_list[j][0]  # category-list의 첫번째 원소들이 category
    return food_category


def find_inform(sentence):

    question_food_category = []
    question_place_name = []

    for food in datas.food_list:
        if food in sentence:
            kind = food_category(food)
            question_food_category.append(kind)

    question_food_category = list(set(question_food_category))  # 중복제거

    for place in datas.place_list:
        if place in sentence:
            question_place_name.append(place)

    return question_food_category, question_place_name


if __name__ == "__main__":
    category, place = find_inform("광화문에 한식 특히 고기맛집 있나요?")