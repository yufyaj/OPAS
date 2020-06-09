import datetime

# ログ出力
def OutLog(output):
    with open("./web_access.log", mode='a') as f:
        f.write(Now() + " " + output + "\n")

# 現在の時刻を取得
def Now():
    return datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')