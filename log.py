import datetime

# ログ出力
def OutLog(output):
    print(Now() + " " + output)

# 現在の時刻を取得
def Now():
    return datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')