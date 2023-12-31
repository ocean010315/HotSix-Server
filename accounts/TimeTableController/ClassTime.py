# 요일 : 월요일 ~ 일요일
DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
# 시간 : 1 ~ 48 = 0:00 ~ 23:59
CLASS_TIMES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
                37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]

def common_class_table(class_tables):
    common_table = ClassTable()
    for time in range(len(CLASS_TIMES)):
        for day in range(len(DAYS)):
            for table in class_tables:
                if table.isFilled(time, day):
                    common_table.setFilled(time, day)
                    break
    return common_table


def class_table_of(table):
    class_table = ClassTable()
    for time in range(len(CLASS_TIMES)):
        for day in range(len(DAYS)):
            if len(table) <= time:
                continue
            if len(table[0]) <= day:
                continue
            if table[time][day] == 1:
                class_table.setFilled(time, day)
    return class_table

# 시간표 객체
class ClassTable:
    # 시간과 요일을 통해 이차원 배열로 초기화
    def __init__(self):
        self.table = [[0 for _ in range(len(DAYS))] for _ in range(len(CLASS_TIMES))]

    # 일정 채우기
    def setFilled(self, time, day):
        self.table[time][day] = 1

    # 일정 유무 확인
    def isFilled(self, time, day):
        if len(self.table) <= time:
            return False
        if len(self.table[0]) <= day:
            return False
        return self.table[time][day] == 1

    # 시간표 이차원 배열 출력
    def print(self):
        count = 0
        for i in self.table:
            print(f"{count} : ", end='\t')
            for j in i:
                print(j, end=' ')
            count += 0.5
            print()