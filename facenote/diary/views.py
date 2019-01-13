from django.shortcuts import render
from django.http import HttpResponse
import MongoConn
from facenote import wechat
from datetime import datetime
from bson import json_util, objectid
import logging
import json

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s %(levelname)s %(message)s',
    filename = './djangoLog.log',)

def index(request):
    return HttpResponse("diary app")

def get_banner(request):
    if request.method == 'GET':
        res = []
        items = MongoConn.find('banner', None)
        for item in items:
            tmp = {}
            tmp['id'] = item['_id']
            tmp['image'] = item['image']
            tmp['url'] = item['url']
            res.append(tmp)

        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')
        
#     if request.method == 'POST':
#         res = {}
#         print(request.POST)
#         print(request.GET)
#         # res['token'] = request.POST.get('code', 'defaultcode')
#         # res['name'] = request.POST.get('name', 'defaultname')
#         # res['passwd'] = request.POST.get('passwd')
#         #res['_id'] = 'asdasd123ad12'
#         # MongoConn.insert('skinrec', res)
#         # wechat.get_openid('ronghao')
#         code = request.POST.get('code')
#         openid, session_key = wechat.get_openid(code)
#         token = wechat.get_token(openid + session_key)
#         res['token'] = token
#         # res['user_id'] = openid
#         #logging.info(token)
#         return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')
