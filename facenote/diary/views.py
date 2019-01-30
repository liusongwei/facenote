from django.shortcuts import render
from django.http import HttpResponse
from facenote.settings import UNKNOWN, UNLOGIN, OK, PARAMERR, PUBLISHLIMIT
from pymongo import DESCENDING, ASCENDING
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
        
        logging.info(pic_file.name)
        tail = '.' + pic_file.name.split('.')[-1]
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

def user_record(request):
    if request.method == 'GET':
        res = {}
        token = request.GET.get('token', None)
        db = MongoConn.find_one('token_ttl', {'token' : token})
        if not db:
            res['errcode'] = UNLOGIN
            return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')
        openid = db.get('openid')

        db_record = MongoConn.find_one('user_record', {'_id' : openid})
        res['pic_num'] = db_record.get('record_pic_num', 0)
        res['day_count'] = db_record.get('record_days_num', 0)
        res['product_count'] = db_record.get('product_record_num', 0)
        db_time = db_record.get('last_record_time', None)
        if db_time:
            last_record_time = db_time + datetime.timedelta(hours = 8)
            # last_record_time = db_time
            res['last_record_time'] = int(time.mktime(last_record_time.timetuple()))
        else:
            res['last_record_time'] = 0

        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')


def upload_product_record(request):
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
        token = req.get('token', None)
        product_name = req.get('product_name', None)
        product_image = req.get('product_image', None)
        product_tags = req.get('product_tags', None)
        skin_images = req.get('skin_images', None)
        summary_tags = req.get('summary_tags', None)

        if not product_name or not product_image or not skin_images or len(skin_images) < 1 or len(skin_images) > 2:
            res['errcode'] = PARAMERR
            return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

        db = MongoConn.find_one('token_ttl', {'token' : token})
        if not db:
            res['errcode'] = UNLOGIN
            return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')
        openid = db.get('openid')

        update_tags_frequency(product_tags, summary_tags)

        today = datetime.datetime.now().strftime("%Y%m%d")
        skin_record = {}
        skin_record['pics'] = skin_images
        skin_record['tags'] = summary_tags
        # skin_record['create_time'] = today
        skin_record['create_time'] = datetime.datetime.utcnow()

        skin_record_id = MongoConn.insert('skin_record', skin_record)

        # tmp_time = MongoConn.find_one('skin_record', {'_id' : ObjectId(skin_record_id)}).get('create_time') + datetime.timedelta(hours = 8)
        # res['time'] = time.mktime(tmp_time.timetuple())

        product_record = {}
        product_record['name'] = product_name
        product_record['image'] = product_image
        product_record['tags'] = product_tags
        product_record['skin_record'] = []
        product_record['skin_record'].append(str(skin_record_id))
        product_record['create_time'] = datetime.datetime.utcnow()
        

        product_record_id = MongoConn.insert('product_record', product_record)

        update_publish_limit(openid, product_record_id, skin_record_id)

        # record_limit = {}
        # record_limit['open_id'] = openid
        # record_limit['product_record_id'] = str(product_record_id)
        # record_limit['skin_record_id'] = str(skin_record_id)
        # record_limit['date'] = today

        # MongoConn.insert('record_limit', record_limit)


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
            db_record['record_days_num'] = days_num
            db_record['record_pic_num'] += len(skin_images)
            db_record['product_record'].append(str(product_record_id))
            db_record['last_record_time'] = datetime.datetime.utcnow()

            MongoConn.save('user_record', db_record)

        res['product_record_id'] = str(product_record_id)
        res['errcode'] = OK


        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

#返回真说明check通过，可以添加skin_record
def check_publish_limit(openid, product_record_id):
    today = datetime.datetime.now().strftime("%Y%m%d")
    res = MongoConn.find_one('record_limit', {'open_id':openid, 'product_record_id':product_record_id, 'date':today})
    if res:
        return False
    else:
        return True

def update_publish_limit(openid, product_record_id, skin_record_id):
    today = datetime.datetime.now().strftime("%Y%m%d")
    record_limit = {}
    record_limit['open_id'] = openid
    record_limit['product_record_id'] = str(product_record_id)
    record_limit['skin_record_id'] = str(skin_record_id)
    record_limit['date'] = today
    MongoConn.insert('record_limit', record_limit)

def update_tags_frequency(effect_tags, summary_tags):
    if effect_tags:
        for tag in effect_tags:
            if MongoConn.find_one('effect_tags', {'_id' : str(tag)}):
                MongoConn.update('effect_tags', {'_id' : str(tag)}, {'$inc' : {'use_count' : 1}})
            else:
                res = {}
                res['_id'] = str(tag)
                res['use_count'] = 1
                MongoConn.insert('effect_tags', res)
    if summary_tags:
        for tag in summary_tags:
            if MongoConn.find_one('summary_tags', {'_id' : str(tag)}):
                MongoConn.update('summary_tags', {'_id' : str(tag)}, {'$inc' : {'use_count' : 1}})
            else:
                res = {}
                res['_id'] = str(tag)
                res['use_count'] = 1
                MongoConn.insert('summary_tags', res)

def upload_skin_record(request):
    if request.method == 'POST':
        res = {}
        req = json.loads(request.body)
        logging.info(req)
        token = req.get('token', None)
        product_record_id = req.get('product_record_id', None)
        skin_images = req.get('skin_images', None)
        summary_tags = req.get('summary_tags', None)

        if not token or not product_record_id or not skin_images or len(skin_images) < 1 or len(skin_images) > 2:
            res['errcode'] = PARAMERR
            return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

        db = MongoConn.find_one('token_ttl', {'token' : token})
        if not db:
            res['errcode'] = UNLOGIN
            return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')
        openid = db.get('openid')

        update_tags_frequency(None, summary_tags)

        # today = datetime.datetime.now().strftime("%Y%m%d")
        if not check_publish_limit(openid, product_record_id):
            res['errcode'] = PUBLISHLIMIT
            return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

        skin_record = {}
        skin_record['pics'] = skin_images
        skin_record['tags'] = summary_tags
        # skin_record['create_time'] = today
        skin_record['create_time'] = datetime.datetime.utcnow()

        skin_record_id = MongoConn.insert('skin_record', skin_record)

        db_product_record = MongoConn.find_one('product_record', {'_id' : ObjectId(product_record_id)})
        db_skin_record_list = db_product_record.get('skin_record', None)
        if db_skin_record_list:
            db_skin_record_list.append(str(skin_record_id))
            MongoConn.save('product_record', db_product_record)
        else:
            res['errcode'] = PARAMERR
            return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')


        update_publish_limit(openid, product_record_id, skin_record_id)

        res['errcode'] = OK
        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

def user_record_list(request):
    if request.method == 'GET':
        res = []
        token = request.GET.get('token', None)
        db = MongoConn.find_one('token_ttl', {'token' : token})
        if not db:
            tmp = {}
            tmp['errcode'] = UNLOGIN
            return HttpResponse(json_util.dumps(tmp,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')
        openid = db.get('openid')

        product_record_list = MongoConn.find_one('user_record', {'_id' : openid}).get('product_record', None)
        if not product_record_list:
            return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

        logging.info(product_record_list)
        for product_record_id in product_record_list:
            logging.info(product_record_id)
            product_record = MongoConn.find_one('product_record', {'_id' : ObjectId(product_record_id)})
            if product_record:
                logging.info(product_record)
                tmp = {}
                tmp['product_id'] = product_record_id
                tmp['product_name'] = product_record.get('name', None)
                tmp['product_image'] = product_record.get('image', None)
                tmp['product_tags'] = product_record.get('tags', None)
                db_create_time = product_record.get('create_time', None)
                if not db_create_time:
                    tmp['create_time'] = None
                else:
                    # logging.info(create_time)
                    create_time = db_create_time + datetime.timedelta(hours = 8)
                    # logging.info(create_time)
                    # create_time = db_create_time  
                    tmp['create_time'] = int(time.mktime(create_time.timetuple()))

                db_skin_record_list = product_record.get('skin_record', None)
                skin_record_len = len(db_skin_record_list)
                skin_record_new_id = db_skin_record_list[0]
                skin_record_old_id = db_skin_record_list[skin_record_len - 1]

                skin_record_new = MongoConn.find_one('skin_record', {'_id' : ObjectId(skin_record_new_id)})
                skin_record_old = MongoConn.find_one('skin_record', {'_id' : ObjectId(skin_record_old_id)})

                if skin_record_new and skin_record_old:
                    tmp['skin_record'] = {}
                    tmp['skin_record']['skin_record_new_iamge'] = skin_record_new.get('pics')[0]
                    skin_record_db_create_time = skin_record_new.get('create_time', None)
                    if not skin_record_db_create_time:
                        tmp['skin_record']['skin_record_new_create_time'] = None
                    else:
                        skin_record_new_create_time = skin_record_db_create_time + datetime.timedelta(hours = 8)
                        # skin_record_new_create_time = skin_record_db_create_time
                        tmp['skin_record']['skin_record_new_create_time'] = int(time.mktime(skin_record_new_create_time.timetuple()))

                    tmp['skin_record']['skin_record_old_iamge'] = skin_record_old.get('pics')[0]
                    skin_record_db_create_time = skin_record_old.get('create_time', None)
                    if not skin_record_db_create_time:
                        tmp['skin_record']['skin_record_old_create_time'] = None
                    else:
                        skin_record_old_create_time = skin_record_db_create_time + datetime.timedelta(hours = 8)
                        # skin_record_old_create_time = skin_record_db_create_time
                        tmp['skin_record']['skin_record_old_create_time'] = int(time.mktime(skin_record_old_create_time.timetuple()))
                
                res.append(tmp)

        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

def get_hot_tags(request):
    if request.method == 'GET':
        res = {}
        token = request.GET.get('token', None)
        db = MongoConn.find_one('token_ttl', {'token' : token})
        if not db:
            tmp = {}
            tmp['errcode'] = UNLOGIN
            return HttpResponse(json_util.dumps(tmp,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

        effect_tags = MongoConn.find('effect_tags', None).sort('use_count', DESCENDING).limit(15)
        summary_tags = MongoConn.find('summary_tags', None).sort('use_count', DESCENDING).limit(15)

        res['effect_tags'] = []
        res['summary_tags'] = []

        for tag in effect_tags:
            res['effect_tags'].append(tag.get('_id', None))
        for tag in summary_tags:
            res['summary_tags'].append(tag.get('_id', None))

        res['errcode'] = OK

        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

def get_compare_pics(request):
    if request.method == 'GET':
        res = []
        token = request.GET.get('token', None)
        product_id = request.GET.get('product_id', None)

        db = MongoConn.find_one('token_ttl', {'token' : token})
        if not db:
            tmp = {}
            tmp['errcode'] = UNLOGIN
            return HttpResponse(json_util.dumps(tmp,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

        product_record = MongoConn.find_one('product_record', {'_id' : ObjectId(product_id)})
        if not product_record:
            tmp = {}
            tmp['errcode'] = UNKNOWN
            return HttpResponse(json_util.dumps(tmp,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')

        db_skin_record_id_list = product_record.get('skin_record', None)
        for skin_record_id in db_skin_record_id_list:
            skin_record = MongoConn.find_one('skin_record', {'_id' : ObjectId(skin_record_id)})
            tmp = {}
            tmp['skin_record_id'] = str(skin_record.get('_id'))
            tmp['image'] = skin_record.get('pics')[0]
            skin_record_db_create_time = skin_record.get('create_time', None)
            if not skin_record_db_create_time:
                tmp['create_time'] = None
            else:
                skin_record_create_time = skin_record_db_create_time + datetime.timedelta(hours = 8)
                # skin_record_create_time = skin_record_db_create_time
                tmp['create_time'] = int(time.mktime(skin_record_create_time.timetuple()))
            res.append(tmp)
        
        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/x-www-form-urlencoded;charset=utf-8')
