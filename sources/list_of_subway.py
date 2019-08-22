except_subway_text_name = "./datas/subway_place_name.csv"
subway_file = "./datas/subway_station.txt"


def set_data(line):
    data_divide = line.split(',', maxsplit=3) 
    place = data_divide[1].strip('"')  # data_divide[1] = 역명
    return place


def except_place():
    except_data = []
    file = open(except_subway_text_name, 'r', encoding='utf-8-sig')
    lines = file.read().split('\n')
    for line in lines[1:]:
        data = set_data(line)
        except_data.append(data + "\n")  # 받아온 역명 data append
    except_data = list(set(except_data)) # except_data에 추가
    except_data.sort()
    return except_data


def main():
    subway_station_list = except_place()
    with open(subway_file, 'w') as file:
        file.writelines(subway_station_list)


if __name__ == '__main__':
    main()
