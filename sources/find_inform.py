with open("./datas/food_list.txt", 'r') as file:
    str = file.read()
    food_list = str.split("\n")
    food_list2 = str.split("-")
with open("./datas/place_name.txt", 'r') as file2:
    place_name = file2.read().split('\n')
with open("./datas/subway_station.txt", 'r') as file3:
    subway_name = file3.read().split('\n')
    place_name.extend(subway_name)


def making_divide_list():
    food_list_middle = []
    food_list_middle_two = []
    for i in range(0, 8):
        word = food_list2[i]
        food_list_middle = word.split("\n")
        if food_list_middle[0] == '':
            del food_list_middle[0]
        if food_list_middle[-1] == '':
            del food_list_middle[-1]
        food_list_middle_two.append(food_list_middle)
    return food_list_middle_two


category_list = making_divide_list()


def find_inform(sentence):

    question_food_category = []
    question_place_name = []

    for food in food_list:
        if food in sentence:
            kind = food_category(food)
            question_food_category.append(kind)

    question_food_category = list(set(question_food_category))  # 중복제거

    for place in place_name:
        if place in sentence:
            question_place_name.append(place)

    return question_food_category, question_place_name


def food_category(food_name):
    for j in range(0, 8):
        for k in range(0, len(category_list[j])):
            if food_name == category_list[j][k]:
                food_category = category_list[j][0]
    return food_category


if __name__ == "__main__":
    category, place = find_inform("광화문에 한식 특히 고기맛집 있나요?")
    print(category)
    print(place)
