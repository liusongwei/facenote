from .settings import APPID, SECRET

# 获取openid
 
import requests
import hashlib

def get_openid(code):
    try:
        url = "https://api.weixin.qq.com/sns/jscode2session" + "?appid=" + APPID + "&secret=" + SECRET + "&js_code=" + code + "&grant_type=authorization_code"
        r = requests.get(url)
        print(r.json())
        openid = r.json()['openid']
        session_key = r.json()['session_key']
    except (Exception) as e:
        print("get_openid: ", e)
        raise
    return openid, session_key

def get_token(key):
    print(key)
    return hashlib.md5(key.encode('UTF-8')).hexdigest().upper()