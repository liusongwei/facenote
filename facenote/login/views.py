from django.shortcuts import render
from django.http import HttpResponse
import MongoConn
from facenote import wechat
from datetime import datetime
from bson import json_util, objectid
import datetime
import logging
import json

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s %(levelname)s %(message)s',
    filename = './djangoLog.log',)

def index(request):
    return HttpResponse("login app")

def login(request):
    if request.method == 'GET':
        res = {}
        print(request.GET)
        logging.info(request.META)
        logging.info(request.GET)
        res['name'] = request.GET.get('name', 'defaultname')
        res['passwd'] = request.GET.get('passwd')
        return HttpResponse("get method")
        
    if request.method == 'POST':
        res = {}
        print(request.POST)
        print(request.GET)
        # res['token'] = request.POST.get('code', 'defaultcode')
        # res['name'] = request.POST.get('name', 'defaultname')
        # res['passwd'] = request.POST.get('passwd')
        #res['_id'] = 'asdasd123ad12'
        # MongoConn.insert('skinrec', res)
        # wechat.get_openid('ronghao')
        code = request.POST.get('code')
        openid, session_key = wechat.get_openid(code)
        token = wechat.get_token(openid + session_key)
        res['token'] = token

        now = datetime.datetime.now()
        # expire_time = now + datetime.timedelta(weeks = 1)
        expire_time = now + datetime.timedelta(minutes = 5)
        print(expire_time)

        token_ttl = {}
        token_ttl['token'] = token
        token_ttl['openid'] = openid
        token_ttl['expire_time'] = expire_time

        MongoConn.update('token_ttl', {'openid' : openid}, {'$set' : {'expire_time' : expire_time, 'token' : token}}, True)
        # res['user_id'] = openid
        #logging.info(token)
        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')
        