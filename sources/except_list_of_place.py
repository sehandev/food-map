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


def main():
    except_place()

if __name__ == '__main__':
    main()
