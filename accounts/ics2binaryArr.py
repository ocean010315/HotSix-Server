import math

ENGLISH_DAYS = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SO']

def ics_to_binary_array(file, table):
    # 파일 데이터 분리 => ['주기', '일자', '시작시간', '종료 시간']의 형태
    lines = file # 파일을 리스트 형태로 저장함
    events = []
    event_data = []
    for line in lines:
        if line.startswith('BEGIN:VEVENT'): # 일정 데이터 시작
            event_data=[]
        elif line.startswith('END:VEVENT'): # 일정 데이터 끝 -> 추출한 일정 데이터 추가
            events.append(event_data)
        elif (line.startswith('DTSTART') or # 일정 데이터(시작시간, 종료시간, 주기 및 일자) 분리
            line.startswith('DTEND') or
            line.startswith('RRULE')):
            event_data.append(line)
    
    for event in events:
        for i in range(0, len(event)):
            # ':' 토대로 값 자르기 (DTSTART;TZID=Asia/Seoul:20230512T110000 => 20230512T110000)
            slice_idx = event[i].find(':') + 1 
            event[i] = event[i][slice_idx:] 
            # ';' 토대로 값 자르기 (FREQ=WEEKLY;BYDAY=MO => [FREQ=WEEKLY, BYDAY=MO])
            if 'FREQ' in event[i]: 
                idx = i
                if(event[idx].find(';') != -1): # 주기와 일자 분리
                    temp = event[idx].split(';')
                    event.remove(event[idx])
                    event.insert(0, temp[1])
                    event.insert(0, temp[0])


    # 분리한 데이터를 토대로 이차원 배열로 시간표 구성
    not_weekly = []

    for event in events: # event = ['주기', '일자', '시작시간', '종료 시간']
        if "WEEKLY" in event[0]:
            # 10분 or 15분 단위의 <시작 시간> 확장
            start_time = event[2][-6:-2]
            if int(start_time[2:]) >= 30: start_time = math.floor(int(start_time) / 100) * 100 + 50 # 40분 or 45분 or 50분 (30분 ~ 59분) -> 30분
            else: start_time = math.floor(int(start_time) / 100) * 100 # 10분 or 15분 or 20분 (00분 ~ 29분) -> 정각

            # 10분 or 15분 단위의 <종료 시간> 확장
            end_time = event[3][-6:-2]
            if int(end_time[2:]) <= 30 and int(end_time[2:]) > 0: end_time = math.ceil(int(end_time) / 100) * 100 - 50 # 10분 or 15분 or 20분 (1분 ~ 30분) -> 30분
            else: end_time = math.ceil(int(end_time) / 100) * 100 # 40분 or 45분 or 50분 (31분 ~ 59분 + 00분) -> 정각

            # 시간표 이차원 배열로 구성
            days = event[1][6:].split(',') # 일자
            start_idx = int(start_time / 50) # math.ceil(start_time / 50) # 시작 시간 -> 시작 인덱스 
            end_idx = int(end_time / 50) # math.ceil(end_time / 50) # 종료 시간 -> 종료 인덱스
            for ch_day in days:
                day = ENGLISH_DAYS.index(ch_day)
                for time in range(start_idx, end_idx):
                    table[time][day] = 1

        else: # 주기 = 1개월 or 1년 or 하루
            not_weekly.append(event)

    return table, not_weekly

# # 사용 예시
# ics_file_path = 'backend\skatkdddnjs1@gmail.com.ics'
# binary_array = ics_to_binary_array(ics_file_path)
