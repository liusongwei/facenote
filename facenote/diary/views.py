from django.shortcuts import render
from django.http import HttpResponse
from facenote.settings import UNKNOWN, UNLOGIN, OK, PARAMERR
import os
import MongoConn
from facenote import wechat
from bson import json_util
from bson.objectid import ObjectId
import datetime
import time
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
        logging.info(request.POST)
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
            
        file_path = os.path.join(dir_path, pic_name+time+tail).replace('\\', '/')
        destination = open(file_path, 'wb+')

        for chunk in pic_file.chunks():
            destination.write(chunk)
        destination.close()

        res['errcode'] = OK
        res['url'] = os.path.join("images", "diary", openid, today, pic_name+time+tail).replace('\\', '/')
        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

def upload_diary(request):
    if request.method == 'POST':
        res = {}
        # logging.info(request.POST)
        # token = request.POST.get('token')
        # product_name = request.POST.get('product_name', None)
        # product_image = request.POST.get('product_image', None)
        # product_tags = request.POST.get('product_tags', None)
        # skin_images = request.POST.get('skin_images', None)
        # summary_tags = request.POST.get('summary_tags', None)

        req = json.loads(request.body)
        logging.info(req)
        token = req['token']
        product_name = req['product_name']
        product_image = req['product_image']
        product_tags = req['product_tags']
        skin_images = req['skin_images']
        summary_tags = req['summary_tags']

        if not product_name or not product_image or not skin_images or len(skin_images) < 1:
            res['errcode'] = PARAMERR
            return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

        db = MongoConn.find_one('token_ttl', {'token' : token})
        if not db:
            res['errcode'] = UNLOGIN
            return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')
        openid = db.get('openid')

        today = datetime.datetime.now().strftime("%Y%m%d")
        skin_record = {}
        skin_record['pics'] = skin_images
        skin_record['tags'] = summary_tags
        skin_record['create_time'] = today

        skin_record_id = MongoConn.insert('skin_record', skin_record)

        # tmp_time = MongoConn.find_one('skin_record', {'_id' : ObjectId(skin_record_id)}).get('create_time') + datetime.timedelta(hours = 8)
        # res['time'] = time.mktime(tmp_time.timetuple())

        product_record = {}
        product_record['name'] = product_name
        product_record['image'] = product_image
        product_record['tags'] = product_tags
        product_record['skin_record'] = []
        product_record['skin_record'].append(str(skin_record_id))

        product_record_id = MongoConn.insert('product_record', product_record)

        record_limit = {}
        record_limit['open_id'] = openid
        record_limit['product_record_id'] = str(product_record_id)
        record_limit['skin_record_id'] = str(skin_record_id)
        record_limit['date'] = today

        MongoConn.insert('record_limit', record_limit)


        days = MongoConn.find('record_limit', {'open_id':openid}).distinct('date')
        days_num = len(days)
        # days_num = MongoConn.distinct('record_limit', 'date', {'open_id' : openid})
        logging.info(days_num)
        user_record = {}
        user_record['_id'] = openid
        user_record['product_record_num'] = 1
        user_record['record_days_num'] = days_num
        user_record['record_pic_num'] = len(skin_images)
        user_record['product_record'] = []
        user_record['product_record'].append(str(product_record_id))
        user_record['last_record_time'] = datetime.datetime.utcnow()

        db_record = MongoConn.find_one('user_record', {'_id' : openid})
        if not db_record:
            MongoConn.insert('user_record', user_record)
        else:
            db_record['product_record_num'] += 1
            # days_num = MongoConn.find_one('record_limit', {'openid':openid, 'product_record_id':product_record_id, 'date':date})
            db_record['record_days_num'] += 1
            db_record['record_pic_num'] += len(skin_images)
            db_record['product_record'].append(str(product_record_id))
            db_record['last_record_time'] = datetime.datetime.utcnow()

            MongoConn.save('user_record', db_record)

        res['product_record_id'] = str(product_record_id)
        res['errcode'] = OK


        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

#返回真说明check通过，可以添加skin_record
def check_publish_limit(openid, product_record_id, date):
    res = MongoConn.find_one('record_limit', {'openid':openid, 'product_record_id':product_record_id, 'date':date})
    if res:
        return False
    else:
        return True