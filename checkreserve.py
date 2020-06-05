from bs4 import BeautifulSoup
import getcode

def CheckReserve(resp, code, day, time):
    day = day[0:4] + "年" + str(int(day[4:6])) + "月"
    time = getcode.GetReserveTime(time)[0:2] + ":00"
    
    src = BeautifulSoup(resp.text, 'html.parser')
    
    table = src.findAll('table')[2]
    lists = table.findAll('tr')
    lists.pop(0)
    lists.pop(0)
    
    
    for list in lists:
        # 体育館コードの取得
        js = list['onclick']
        start = js.find('Enter') + 8
        finish = js.find(')', start) - 1
        src_code = js[start:finis]
        
        # 月日の取得
        src_day = list.findAll('td')[0].get_text()
        src_day = src_day.replace("\r", "").replace("\t", "").replace("\n", "")
        finish = src_day.find('(')
        src_day = src_day[0:finish]
        
        # 時間の取得
        src_time = list.findAll('td')[2].get_text()
        src_time = src_time.replace("\r", "").replace("\t", "").replace("\n", "")
        src_time = src_time[0:5]
        
        if (code[0:13] == src_code[0:13] And day == src_day And time == src_time):
            return true
    
    return false


