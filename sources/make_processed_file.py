import re
from twkorean import TwitterKoreanProcessor
import manage_file, preprocessing

processor = TwitterKoreanProcessor()
hangul = re.compile("[^ 가-힣]+")

origin_file = "./datas/kakao.txt"
result_file = "./results/processed.txt"

origin_list = preprocessing.preprocessing(origin_file)
result = []
for i in range(len(origin_list)):
    origin_list[i][2] = hangul.sub(" ", origin_list[i][2])
    tokens = processor.tokenize_to_strings(origin_list[i][2])
    result.append(str(tokens))
manage_file.save_list_as_file(result_file, result)
