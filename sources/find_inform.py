# from sources import

def find_inform(sentence):    
    with open("../datas/food_list.txt", 'r') as file:
        food_list = file.read().split("\n")
    with open("../datas/place_name.txt", 'r') as file2:
        place_name = file2.read().split('\n')
    with open("../datas/subway_station.txt", 'r') as file3:
        subway_name = file3.read().split('\n')

    place_name.extend(subway_name)
    question_food_category = []
    question_place_name = []

    question = sentence.split(" ")
    print(question)
    # datas에서 place_name, food_list 필요함

    for i in range(0, len(question)):
        if question[i] in food_list:
            kind = food_category(question[i])
            question_food_category.append(kind)
        elif question[i] in place_name:
            question_place_name.append(question[i])

    return question_food_category, question_place_name


def food_category(food_name):
    food_category = []
    count = -1
    with open("../datas/food_list.txt", 'r') as file:
        food_list = file.read().split("-")
    for i in range(0, len(food_list)):
        food = food_list[i]
        food_category = food.split("\n")
        for j in range(0, len(food_category)):
            food_category[j] = food_category[j].strip()
        print(food_category[i])
    
    
if __name__ == "__main__":
    find_inform("광화문 에 한식 특히 고기 맛집 있나요 ?")