from django.shortcuts import render
from django.http import HttpResponse
from MongoConn import *
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
        res['name'] = request.POST.get('name', 'defaultname')
        res['passwd'] = request.POST.get('passwd')
        # res['_id'] = 'asdasd123ad12'
        insert('skinrec', res)
        # return HttpResponse("post method")
        return HttpResponse(json_util.dumps(res,ensure_ascii=False),content_type='application/json;charset=utf-8')
