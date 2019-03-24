# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime


# Create your models here.

class UploadRecord(models.Model):
    upload_time = models.DateTimeField(auto_created=True)
    excel_file = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=30)


class Person(models.Model):
    SEX_CHOICES = (
        (True, '男'),
        (False, '女')
    )
    name = models.CharField(max_length=30)
    id_num = models.CharField(max_length=18)
    sex = models.BooleanField(choices=SEX_CHOICES)
    birthday = models.DateField()
    create_time = models.DateTimeField(auto_created=True)


