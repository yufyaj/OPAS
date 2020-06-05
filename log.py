import datetime

# ƒƒOo—Í
def OutLog(output):
    print(Now() + " " + output)

# Œ»İ‚Ì‚ğæ“¾
def Now():
    return datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')