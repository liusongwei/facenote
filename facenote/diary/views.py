from django.shortcuts import render
from django.http import HttpResponse
from facenote.settings import UNKNOWN, UNLOGIN, OK
import os
import MongoConn
from facenote import wechat
from bson import json_util, objectid
import datetime
import logging
import json

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s %(levelname)s %(message)s',
    filename = './djangoLog.log',)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
            logging.info(tmp)

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

def upload_pic(request):
    if request.method == 'POST':
        res = {}
        logging.info(request.GET)
        token = request.GET.get('token')
        pic_name = request.GET.get('name')
        pic_file = request.FILES.get(pic_name)

        db = MongoConn.find_one('token_ttl', None, {'token' : token})
        if not db:
            res['errcode'] = UNLOGIN
            return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')
        openid = db.get('openid')

        if not pic_file:
            res['errcode'] = UNKNOWN
            return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

        # today = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        today = datetime.datetime.now().strftime("%Y%m%d")
        time = datetime.datetime.now().strftime("%H%M%S")
        
        tail = '.' + pic_file.name.split('.')[1]
        dir_path = os.path.join(BASE_DIR, "common_static", "images", "diary", openid, today).replace('\\', '/')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
        file_path = os.path.join(BASE_DIR, "common_static", "images", "diary", openid, today, pic_name+time+tail).replace('\\', '/')
        destination = open(file_path, 'wb+')

        for chunk in pic_file.chunks():
            destination.write(chunk)
        destination.close()

        res['errcode'] = OK
        res['url'] = os.path.join("images", "diary", openid, today, pic_name+time+tail).replace('\\', '/')
        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')
