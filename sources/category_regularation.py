from sources import datas


def find_category(pre_category):
    # 네이버 카테고리가 들어오면 정해진 카테고리로 변경

    categories = pre_category.split('>')
    if len(categories) < 2:
        return pre_category
    else:
        new_category = categories[0]
        if categories[0] == "음식점":
            new_category = find_category(categories[1])
        elif categories[0] == "중식당":
            new_category = "중식"
        else:
            for category in categories:
                for tmp_list in datas.food_category_list:
                    if category in tmp_list:
                        new_category = tmp_list[0]

        return new_category


if __name__ == "__main__":
    print(find_category("음식점>한식"))
    print(find_category("한식>한정식"))
    print(find_category("음식점>베트남음식"))
