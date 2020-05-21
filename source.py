import os
import requests

os.environ["http_proxy"] = "http://17017:17@01Tc7@proxy:8000"

# データをポストする為の関数(戻り値は　レスポンス, 次回リファラー）
def PostData(sess, url, referrer, sessID, data = None):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": sessID + " ROUTEID=.r1; vyrqgyw=RIYOSHA-WEB4; _ga=GA1.3.1548849856.1589966404; _gid=GA1.3.1489916570.1589966404; _gat_UA-123480356-1=1",
        "Host": "reserve.opas.jp",
        "Origin": "https://reserve.opas.jp",
        "Referer": referrer,
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
    }
    
    # データがある場合と無い場合で変える
    if (data is None):
        resp = sess.post(url, headers=headers)
    else:
        resp = sess.post(url, headers=headers, data=data)
    
    # 結果のエンコードを適正に
    resp.encoding = resp.apparent_encoding
    
    return resp, url;

# セッションIDの取得
def GetSessionID(resp):
    start  = resp.headers['Set-Cookie'].find("JSESSIONID=", 2)
    finish = resp.headers['Set-Cookie'].find(";", start)
    sessID = resp.headers['Set-Cookie'][start:finish+1]
    
    return sessID

# ログアウト
def LogOut(sess, sessID):
    url = "https://reserve.opas.jp/osakashi/menu/Logout.cgi"
    PostData(sess, url, "", sessID)

sess = requests.session()
sessID = "JSESSIONID=93B4E881360AE1D3B6CEBBF15366A947;"
referrer = "https://reserve.opas.jp/osakashi/menu/Logout.cgi"

# ログイン
url = "https://reserve.opas.jp/osakashi/menu/Login.cgi"
data = {
    "action": "Enter",
    "txtProcId": "%2Fmenu%2FLogin",
    "txtRiyoshaCode": "27038790",
    "txtPassWord": "WYDHF8VG",
}

resp, referrer = PostData(sess, url, referrer, sessID, data)
sessID = GetSessionID(resp)


# メニューを開く
url = "https://reserve.opas.jp/osakashi/menu/Menu.cgi"
data = {
    "action":"Enter",
    "txtProcId":"/menu/Menu",
    "txtFunctionCode":"Yoyaku"
}

resp, referrer = PostData(sess, url, referrer, sessID, data)


# 空き状況照会
url = "https://reserve.opas.jp/osakashi/yoyaku/QueryMethodSelect.cgi"
data = {
    "action":"Enter",
    "txtProcId":"/yoyaku/QueryMethodSelect",
    "txtSelectKey":"0"
}

resp, referrer = PostData(sess, url, referrer, sessID, data)


# 大分類選択
url = "https://reserve.opas.jp/osakashi/yoyaku/GenreSelect.cgi"

data = {
    "action":"Enter",
    "txtProcId":"/yoyaku/GenreSelect",
    "gamenNo":"0",
    "metaShubetsuCd":["C00","","","","","","","","","","","","","",""]
}

resp, referrer = PostData(sess, url, referrer, sessID, data)


# 小分類選択
data = {
    "action":"Enter",
    "txtProcId":"/yoyaku/GenreSelect",
    "gamenNo":"1",
    "shubetsuCd":"C01"
}

resp, referrer = PostData(sess, url, referrer, sessID, data)


# 体育館選択
url = "https://reserve.opas.jp/osakashi/yoyaku/ShisetsuMultiSelect.cgi"
data = {
    "action":"Enter",
    "txtProcId":"/yoyaku/ShisetsuMultiSelect",
    "checkMeisaiUniqKey2[0]":"",
    "checkMeisaiUniqKey2[1]":"",
    "checkMeisaiUniqKey2[2]":"",
    "checkMeisaiUniqKey2[3]":"",
    "checkMeisaiUniqKey2[4]":"",
    "checkMeisaiUniqKey2[5]":"",
    "checkMeisaiUniqKey2[6]":"",
    "checkMeisaiUniqKey2[7]":"",
    "checkMeisaiUniqKey2[8]":"",
    "checkMeisaiUniqKey2[9]":"",
    "checkMeisaiUniqKey2[10]":"",
    "checkMeisaiUniqKey2[11]":"",
    "checkMeisaiUniqKey2[12]":"",
    "checkMeisaiUniqKey2[13]":"",
    "checkMeisaiUniqKey2[14]":"",
    "checkMeisaiUniqKey2[15]":"",
    "checkMeisaiUniqKey2[16]":"",
    "checkMeisaiUniqKey2[17]":"",
    "checkMeisaiUniqKey2[18]":"",
    "checkMeisaiUniqKey2[19]":"",
    "checkMeisaiUniqKey2[20]":"",
    "checkMeisaiUniqKey2[21]":"",
    "checkMeisaiUniqKey2[22]":"",
    "checkMeisaiUniqKey2[23]":"",
    "checkMeisaiUniqKey2[24]":"",
    "checkMeisaiUniqKey2[25]":"",
    "checkMeisaiUniqKey2[26]":"",
    "checkMeisaiUniqKey2[27]":"",
    "checkMeisaiUniqKey2[28]":"",
    "checkMeisaiUniqKey2[29]":"",
    "checkMeisaiUniqKey2[30]":"",
    "checkMeisaiUniqKey2[31]":"",
    "checkMeisaiUniqKey2[32]":"",
    "checkMeisaiUniqKey2[33]":"",
    "checkMeisaiUniqKey2[34]":"",
    "checkMeisaiUniqKey2[35]":"",
    "checkMeisaiUniqKey2[36]":"",
    "checkMeisaiUniqKey":["","","","","","","","","","","","","271004_001_20_01_01_001_001","","","","","","","","","","","","","","","","","","","","","","","",""]
}

resp, referrer = PostData(sess, url, referrer, sessID, data)


# 日付表示
url = "https://reserve.opas.jp/osakashi/yoyaku/CalendarStatusSelect.cgi"
data = {
    "action":"Setup",
    "txtProcId":"/yoyaku/CalendarStatusSelect",
    "txtCalYobiView":"block",
    "printedFlg":"",
    "radioshow":"week",
    "optYear":"2020",
    "optMonth":"06",
    "optDay":"20",
    "txtYear":"",
    "txtMonth":"",
    "txtDay":"",
    "checkShowDay":["MON","TUE","WED","THU","FRI","SAT","SUN","HOL"]
}

resp, referrer = PostData(sess, url, referrer, sessID, data)

# 日付選択
url = "https://reserve.opas.jp/osakashi/yoyaku/CalendarStatusSelect.cgi"
data = {
    "action":"Enter",
    "txtProcId":"/yoyaku/CalendarStatusSelect",
    "txtCalYobiView":"block",
    "printedFlg":"",
    "radioshow":"week",
    "optYear":"2020",
    "optMonth":"06",
    "optDay":"20",
    "txtYear":"",
    "txtMonth":"",
    "txtDay":"",
    "checkShowDay":["MON","TUE","WED","THU","FRI","SAT","SUN","HOL"],
    "checkYoyakuStatus":["271004_001_20_01_01_0000_20200623_1:1_0_1_1_0903","","","","","",""]
}

resp, referrer = PostData(sess, url, referrer, sessID, data)
