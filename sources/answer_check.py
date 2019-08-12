from sources import naver_local

def location_find(restaurant_list, name, places):
    # 식당명 검색결과와 함께 지역명 list가 들어오면 지역명과 함께 검색해서 우선순위 변경
    for place in places:
        another_name = name + " " + place
        location_result = naver_local.check_name(another_name, name)
        if location_result != []:
            # 검색결과가 있으면
            new_first = []
            for location_restaurants in location_result:
                # 검색결과의 1, 2, 3순위에서
                for restaurant in location_restaurants:
                    # 각 식당이 원래 검색결과에 있으면 1순위로 올리기
                    for tmp_list in restaurant_list:
                        if restaurant in tmp_list:
                            new_first.append(restaurant)
                            tmp_list.remove(restaurant)

            restaurant_list[1].extend(restaurant_list[0])
            restaurant_list[0] = new_first

            return restaurant_list, place

    return restaurant_list, ""
