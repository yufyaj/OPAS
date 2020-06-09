from bs4 import BeautifulSoup
from . import getcode

def CheckReserve(resp, code, day, time):
    day = day[0:4] + "年" + str(int(day[4:6])) + "月" + str(int(day[6:8])) + "日"
    time = getcode.GetReserveTime(time)[0:2] + ":00"
    
    src = BeautifulSoup(resp.text, 'html.parser')
    
    table = src.findAll('table')[2]
    lists = table.findAll('tr')
    lists.pop(0)
    lists.pop(0)
    lists.pop(len(lists) - 1)
    
    
    for list in lists:
        # 取り消しデータを省く
        str_del = list.findAll('td')[1].get_text()
        if (str_del.find('【取消済み】') != -1):
            continue
        
        # 体育館コードの取得
        js = list['onclick']
        start = js.find('Enter') + 8
        finish = js.find(')', start) - 1
        src_code = js[start:finish]
        
        # 月日の取得
        src_day = list.findAll('td')[0].get_text()
        src_day = src_day.replace("\r", "").replace("\t", "").replace("\n", "")
        finish = src_day.find('(')
        src_day = src_day[0:finish]
        
        # 時間の取得
        src_time = list.findAll('td')[2].get_text()
        src_time = src_time.replace("\r", "").replace("\t", "").replace("\n", "")
        src_time = src_time[0:5]
        
        if (code[0:13] == src_code[0:13] and day == src_day and time == src_time):
            return True
    
    return False


