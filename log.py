import datetime

# ���O�o��
def OutLog(output):
    print(Now() + " " + output)

# ���݂̎������擾
def Now():
    return datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')