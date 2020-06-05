import requests
import log

class session:
    def __init__(self):
        self.sess = requests.session()
        self.sessID = "JSESSIONID=93B4E881360AE1D3B6CEBBF15366A947;"
        self.referrer = "https://reserve.opas.jp/osakashi/menu/Logout.cgi"
        self.url = ""
        self.headers = ""
        self.data = ""
        self.resp = ""
    
    
    # ポストするパラメーターを格納
    def setPostParam(self, param):
        self.url = param[0]
        self.headers = param[1]
        self.data = param[2]
    
    
    # セッションIDを格納
    def setSessionID(self, sessID):
        self.sessID = sessID
    
    
    # データをポストする為の関数(戻り値は　レスポンス, 次回リファラー）
    def PostData(self):
        log.OutLog("URL: " + self.url)
        
        self.resp = self.sess.post(self.url, headers=self.headers, data=self.data)
        
        # 結果のエンコードを適正に
        self.resp.encoding = self.resp.apparent_encoding
        
        self.referrer = self.url