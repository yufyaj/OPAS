


url = "https://reserve.opas.jp/osakashi/menu/Login.cgi"
headers = {
    "Host": "reserve.opas.jp",
    "Connection": "keep-alive",
    "Content-Length": "83",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "https://reserve.opas.jp",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://reserve.opas.jp/osakashi/menu/Logout.cgi",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Cookie": "JSESSIONID=C32EBED1156DAE3A6D143CE69277B370; _ga=GA1.3.902665101.1551087695; ROUTEID=.r2; vyrqgyw=RIYOSHA-WEB5; _gid=GA1.3.755809145.1589872892"
}

data = {
    "action": "Enter",
    "txtProcId": "%2Fmenu%2FLogin",
    "txtRiyoshaCode": "27038790",
    "txtPassWord": "WYDHF8VG",
}

sess = requests.session()
ret = sess.post(url, headers=headers, data=data)

start  = ret.headers['Set-Cookie'].find("JSESSIONID=", 2)
finish = ret.headers['Set-Cookie'].find(";", start)
sessID = ret.headers['Set-Cookie'][start:finish+1]

url = "https://reserve.opas.jp/osakashi/yoyaku/CalendarStatusSelect.cgi"
headers = {
    "Cookie": sessID + " _ga=GA1.3.902665101.1551087695; _gid=GA1.3.755809145.1589872892; vyrqgyw=RIYOSHA-WEB5; _gat_UA-123480356-1=1; ROUTEID=.r2",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://reserve.opas.jp",
    "Content-Length": "83",
    "Accept-Language": "ja-jp",
    "Host": "reserve.opas.jp",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15",
    "Referer": "https://reserve.opas.jp/osakashi/yoyaku/ShinseiEntry.cgi",
    "Accept-Encoding": "br, gzip, deflate",
    "Connection": "keep-alive"
}
data = {
    "checkShowDay": ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN", "HOL"),
    "MIMEタイプ": "application/x-www-form-urlencoded",
    "action": "Enter",
    "txtProcId": "/yoyaku/CalendarStatusSelect",
    "txtCalYobiView": "block",
    "printedFlg": "",
    "radioshow": "week",
    "optYear": "2020",
    "optMonth": "06",
    "optDay": "19",
    "txtYear": "",
    "txtMonth": "",
    "txtDay": "",
    "checkYoyakuStatus": "271004_001_20_01_01_0000_20200624_3:3_0_1_1_1503"
}

ret = sess.post(url, headers=headers, data=data)


ret.encoding = ret.apparent_encoding

