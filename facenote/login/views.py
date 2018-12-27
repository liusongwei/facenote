from django.shortcuts import render
from django.http import HttpResponse
from MongoConn import *
from facenote import wechat
from bson import json_util
import logging
import json

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s %(levelname)s %(message)s',
    filename = './djangoLog.log',)

def index(request):
    return HttpResponse("login app")

def test(request):
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
        res['code'] = request.POST.get('code', 'defaultcode')
        # res['name'] = request.POST.get('name', 'defaultname')
        # res['passwd'] = request.POST.get('passwd')
        #res['_id'] = 'asdasd123ad12'
        #insert('skinrec', res)
        # wechat.get_openid('ronghao')
        #token = wechat.get_token('ronghao')
        #logging.info(token)
        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')
