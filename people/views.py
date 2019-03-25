# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from datetime import datetime
from threading import Thread

from django.db import transaction, DatabaseError
from django.http import JsonResponse
from django.shortcuts import render, redirect

import xlrd

# Create your views here.
from people.models import UploadRecord, Person

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def index(request):
    if request.method == 'GET':
        up_record = UploadRecord.objects.all().order_by('-id')[:5]
        return render(request, 'index.html', {'up_recode': up_record})
    elif request.method == 'POST':
        excel_file = request.FILES['excel']
        now_time = datetime.now()
        UploadRecord(upload_time=now_time, excel_file=excel_file, status='上传成功').save()
        t = MyThread(now_time)
        t.start()
        return redirect('/people/index')


class MyThread(Thread):

    def __init__(self, timestamp):
        super(MyThread, self).__init__()
        self.timestamp = timestamp

    def deal_excel(self):
        print 'hello'
        upload_file = UploadRecord.objects.filter(upload_time=self.timestamp).first()
        file_path = upload_file.excel_file.path
        book = xlrd.open_workbook(file_path)
        for sheet in book.sheets():
            for row in sheet.get_rows():
                try:
                    p_name = row[0].value
                    p_num = row[1].value

                    if p_name == '':
                        break
                    if not str(p_num).isalnum():
                        break
                    birthday_str = p_num[6:14]
                    birthday = datetime.strptime(birthday_str, "%Y%m%d")

                    if int(p_num[16]) % 2 == 0:
                        sex = False
                    else:
                        sex = True

                except Exception as e:
                    logger.error(e)
                    upload_file.status = '解析出错误，请确认表格格式。'
                    upload_file.save()
                else:
                    Person(
                        name=p_name,
                        id_num=p_num,
                        birthday=birthday,
                        sex=sex,
                        create_time=self.timestamp
                    ).save()
        upload_file.status = '解析成功'
        upload_file.save()

    def run(self):
        try:
            with transaction.atomic():
                self.deal_excel()
        except DatabaseError as e:
            logger.error(e)

        return


def get_person_by_time(request):
    if request.method == 'GET':
        get_obj = request.GET
        upload_time = get_obj.get('upload_time')
        if upload_time is not None:
            upload_time = datetime.strptime(upload_time, '%Y-%m-%d %H:%M:%S:%f')
        else:
            ur = UploadRecord.objects.order_by('-id').first()
            upload_time = ur.upload_time
        current_time = get_obj.get('current_time')
        if current_time is not None:
            current_date = datetime.strptime(current_time, '%Y-%m-%d')
        else:
            current_date = datetime.now()
        persons = Person.objects.filter(create_time__gte=upload_time).order_by('id').all()
        data_array = []
        for person in persons:
            born = person.birthday
            current = current_date
            current_age = current.year - born.year - ((current.month, current.day) < (born.month, born.day))
            people = {
                'id': person.id,
                'name': person.name,
                'id_num': person.id_num,
                'sex': '男' if person.sex else '女',
                'birthday': person.birthday,
                'age': current_age
            }
            data_array.append(people)
        data_dict = {
            'code': 0,
            'data': data_array
        }
        return JsonResponse(data_dict)


def get_person_by_age(request):
    data_dict = {}
    if request.method == 'GET':
        get_obj = request.GET
        upload_time = get_obj.get('upload_time')
        if upload_time is not None:
            upload_time = datetime.strptime(upload_time, '%Y-%m-%d %H:%M:%S:%f')
        else:
            ur = UploadRecord.objects.order_by('-id').first()
            upload_time = ur.upload_time
        min_age = get_obj.get('min_age')
        max_age = get_obj.get('max_age')
        if min_age is None:
            data_dict['code'] = 1
            data_dict['msg'] = 'min_age args error'
            return JsonResponse(data_dict)
        if max_age is None:
            data_dict['code'] = 1
            data_dict['msg'] = 'max_age args error'
            return JsonResponse(data_dict)

        if int(min_age) > int(max_age):
            data_dict['code'] = 1
            data_dict['msg'] = 'max_age is small min_age args error'
            return JsonResponse(data_dict)

        now_datetime = datetime.now()
        max_datetime = now_datetime.replace(now_datetime.year-int(min_age))
        min_datetime = now_datetime.replace(now_datetime.year-int(max_age))
        persons = Person.objects.filter(
            create_time=upload_time,
            birthday__gte=min_datetime,
            birthday__lte=max_datetime).order_by('id').all()
        in_count = float(len(persons))
        count_persons = Person.objects.filter(create_time=upload_time).count()
        data_array = []
        for person in persons:
            born = person.birthday
            current = datetime.now()
            current_age = current.year - born.year - ((current.month, current.day) < (born.month, born.day))
            people = {
                'id': person.id,
                'name': person.name,
                'id_num': person.id_num,
                'sex': '男' if person.sex else '女',
                'birthday': person.birthday,
                'age': current_age
            }
            data_array.append(people)
        data_dict = {
            'code': 0,
            'data': data_array,
            'in_total': in_count/count_persons
        }
        return JsonResponse(data_dict)
