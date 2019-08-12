with open("./datas/food_list.txt", 'r') as file:
    food_list = file.read().split("\n")
with open("./datas/place_name.txt", 'r') as file2:
    place_name = file2.read().split('\n')
with open("./datas/subway_station.txt", 'r') as file3:
    subway_name = file3.read().split('\n')


def find_inform(sentence):

    place_name.extend(subway_name)
    question_food_category = []
    question_place_name = []

    category_list = making_divide_list()
    question = sentence.split(" ")

    for i in range(0, len(question)):
        if question[i] in food_list:
            kind = food_category(question[i], category_list)
            question_food_category.append(kind)
        elif question[i] in place_name:
            question_place_name.append(question[i])

    question_food_category = list(set(question_food_category))

    return question_food_category, question_place_name


def food_category(food_name, category_list):
    for j in range(0, 8):
        for k in range(0, len(category_list[j])):
            if food_name == category_list[j][k]:
                food_category = category_list[j][0]
    return food_category


def making_divide_list():
    food_list_middle = []
    food_list_middle_two = []
    with open("./datas/food_list.txt", 'r') as file:
        food_list2 = file.read().split("-")
    for i in range(0, 8):
        word = food_list2[i]
        food_list_middle = word.split("\n")
        if food_list_middle[0] == '':
            del food_list_middle[0]
        if food_list_middle[-1] == '':
            del food_list_middle[-1]
        food_list_middle_two.append(food_list_middle)
    return food_list_middle_two


if __name__ == "__main__":
    find_inform("광화문 에 한식 특히 고기 맛집 있나요 ?")
