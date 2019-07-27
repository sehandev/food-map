from twkorean import TwitterKoreanProcessor
processor = TwitterKoreanProcessor()

print(processor.tokenize_to_strings("괜참ㅎ은거 추천해주실"))

# with open("../datas/kakao_questions.txt", 'r') as file:
#     lines = file.read().split('\n')
#     lines = list(set(lines))
#
# lines.sort(key=len)
#
# with open("../datas/kakao_questions_dup_remove.txt", 'w') as file:
#     for line in lines:
#         tokens = processor.tokenize_to_strings(line)
#         if len(tokens) <= 30:
#             file.write(line + '\n')
#             file.write(str(tokens) + '\n\n')
