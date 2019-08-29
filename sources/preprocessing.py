from sources import datas


def preprocessing():
    new_lines = []  # 새롭게 작성할 문서
    for line in datas.kakao_log[2:]:

        # 빈 줄 제거
        if line == "":
            continue

        # 2018년 8월 19일 일요일
        if 15 <= len(line) <= 18:
            if line[4] == "년" and line[-5] == "일" and line[-2:] == "요일":
                continue

        # 2018. 8. 22. 오후 8:20: sehan님이 들어왔습니다.
        if line[-7:] == "들어왔습니다.":
            continue

        # 2018. 9. 9. 오후 4:21: sehan님이 나갔습니다.
        if line[-6:] == "나갔습니다.":
            continue

        # 2018. 11. 1. 오후 6:39, sehan : 사진
        if line[-5:] == " : 사진":
            continue

        # 운영정책을 위반한 메시지로 신고 접수 시 카카오톡 이용에 제한이 있을 수 있습니다.
        if line == "운영정책을 위반한 메시지로 신고 접수 시 카카오톡 이용에 제한이 있을 수 있습니다.":
            continue

        # 삭제된 메시지입니다.
        if line == "삭제된 메시지입니다.":
            continue

        # 2018. 11. 1. 오후 6:39: 채팅방 관리자가 메시지를 가렸습니다.
        if line[-20:] == "채팅방 관리자가 메시지를 가렸습니다.":
            continue

        # 2018. 11. 1. 오후 6:39: sehan님을 내보냈습니다.
        if line[-10:] == "님을 내보냈습니다.":
            continue

        # 2018. 10. 27. 오후 9:27, 진수성찬 : 톡게시판 '투표': 빕 구르망 투어–교양식사
        if line.count(" : 톡게시판 \'"):
            continue

        line = line.replace("이모티콘", '')

        time_name_log = line.split(',', maxsplit=1)

        # 2018. 8. 18. 오후 6:45, sehan : ㅎㅇ

        if len(time_name_log) > 1:
            time_name_log = [time_name_log[0]] + time_name_log[1].split(' : ', maxsplit=1)
            time_stamp = time_name_log[0]
            if len(time_stamp) >= 2:
                if len(time_stamp.split('.')) == 4:
                    tmp = time_stamp.split('.')[3][1:3]
                    if tmp == "오전" or tmp == "오후":
                        new_lines.append(time_name_log)
                        continue

        new_lines[-1][2] += " " + line  # 채팅에 newline이 있는 경우

    return new_lines
