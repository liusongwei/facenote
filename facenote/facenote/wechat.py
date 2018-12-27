from .settings import APPID, SECRET

# 获取openid
 
import requests
import hashlib

def get_openid(code):
    url = "https://api.weixin.qq.com/sns/jscode2session" + "?appid=" + APPID + "&secret=" + SECRET + "&js_code=" + code + "&grant_type=authorization_code"
    r = requests.get(url)
    print(r.json())
    openid = r.json()['openid']
 
    return openid

def get_token(openid):
    return hashlib.md5(openid).hexdigest().upper()