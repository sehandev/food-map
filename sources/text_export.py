
import pandas as pd


def parsing_word(line):  # 문장쪼개기(함수)
    first_divide = line.split(',', maxsplit=1)  # 시간 / 이름+내용 분리
    time = first_divide[0]  # 분리된 시간 값을 time 변수에 저장
    second_divide = first_divide[1].split(':', maxsplit=1)  # 이름 / 내용 분리
    name = second_divide[0].strip()  # 이름 => name
    text = second_divide[1].replace("이모티콘", "").strip()  # 내용 => text
    word = [name, time, text]  # 이름-시간-내용에 맞춰서 한 배열로 정리
    return word  # 정리된 형식으로 return


def text_export(text_name):
    user_data = []
    file = open(text_name, 'r', encoding='utf-8-sig')
    lines = file.read().split('\n')
    for line in lines[:-1]:
        parse = parsing_word(line)
        user_data.append(parse)

    user_data.sort(key=lambda x: x[0])
    name = user_data[0][0]
    for i in range(1, len(user_data)):  # 중복된 이름이면 지워주고 넘기는 것
        if name in user_data[i][0]:
            user_data[i][0] = user_data[i][0].replace(name, "")
        else:
            name = user_data[i][0]

    data = pd.DataFrame(user_data)
    data.columns = ['이름', '시간', '내용']
    data = data.set_index("이름")

    data.to_csv('../datas/', encoding='euc-kr')


def main():
    text_export("서울시 지하철역 정보 검색()")


if __name__ == '__main__':
    main()
