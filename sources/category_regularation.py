with open("./datas/food_list.txt", 'r') as file:
    food_list = file.read().split("-")

    food_list_middle = []
    food_list_middle_two = []
    for word in food_list:
        food_list_middle = word.split("\n")
        if food_list_middle[0] == '':
            del food_list_middle[0]
        if food_list_middle[-1] == '':
            del food_list_middle[-1]
        food_list_middle_two.append(food_list_middle)

    food_list = food_list_middle_two

def categories_find(dict):
    categories = []
    for data in dict:
        for tt in dict[data]:
            for restaurant in tt:
                categories.extend(restaurant["category"].split('>'))

    categories = list(set(categories))
    categories.sort()
    print(*categories, sep='\n')

def find_category(pre_category):
    # 네이버 카테고리가 들어오면 정해진 카테고리로 변경

    categories = pre_category.split('>')
    new_category = categories[0]
    if categories[0] == "음식점":
        new_category = find_category(categories[1])
    elif categories[0] == "중식당":
        new_category = "중식"
    else:
        for category in categories:
            for tmp_list in food_list:
                if category in tmp_list:
                    new_category = tmp_list[0]

    return new_category

if __name__ == "__main__":
    print(find_category("음식점>한식"))
    print(find_category("한식>한정식"))
    print(find_category("음식점>베트남음식"))