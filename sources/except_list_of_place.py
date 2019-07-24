import requests


except_subway_text_name = "../datas/subway_place_name.csv"

def set_data(line):
    data_divide = line.split(',', maxsplit=3)
    place = data_divide[1].strip('"')
    return place


def except_place():
    except_data = []
    file = open(except_subway_text_name, 'r', encoding='utf-8-sig')
    lines = file.read().split('\n')
    for line in lines[1:-1]:
        data = set_data(line)
        except_data.append(data)
    return except_data


def place_name_list():
    info_key = '4284DB27-53C5-3C33-88E5-EDFA843DA586'
    info_url = 'http://www.sehan.ml'
    need_parameter = '[geomFilter]'
    place_url = 'http://api.vworld.kr/req/data?service=data&request=GetFeature&data=LT_C_ADEMD_INFO&key='+ info_key +'&domain='+ info_url + '&' + need_parameter
    response = requests.get(place_url)

    place = response.text
    print(place)

def main():
    except_place()
    place_name_list()


if __name__ == '__main__':
    main()
