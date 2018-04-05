# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import uuid


# Create your models here.
# 用户表
class User(models.Model):
    uname = models.CharField(max_length=20)
    upasswd = models.CharField(max_length=30)
    udesc = models.CharField(max_length=30)
    isLogin = models.BooleanField(default=False)
    dateTime = models.DateTimeField(auto_now_add=True)
    isDelete = models.BooleanField(default=False)

    def __repr__(self):
        return self.uname


# 主机表
class Host(models.Model):
    hname = models.CharField(max_length=20)
    hstatus = models.CharField(max_length=10)
    haddr = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now_add=True)
    isDelete = models.BooleanField(default=False)
    belong = models.ForeignKey('User')

    def __repr__(self):
        return self.hname


# 模版表
class Template(models.Model):
    tname = models.CharField(max_length=20)
    tcpus = models.IntegerField()
    tmemory = models.IntegerField()
    tuuid = models.UUIDField(default=uuid.uuid1())
    tmac = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now_add=True)
    isDelete = models.BooleanField(default=False)
    timgName = models.ForeignKey('Image')

    def __repr__(self):
        return self.tname


# 镜像表
class Image(models.Model):
    iname = models.CharField(max_length=20)
    iaddr = models.CharField(max_length=50)
    dateTime = models.DateTimeField(auto_now_add=True)
    isDelete = models.BooleanField(default=False)

    def __repr__(self):
        return self.iname

    @classmethod
    def addImageToDB(cls, iname, iaddr):
        image = cls(iname=iname, iaddr=iaddr)
        return image


# 虚拟机表
class VM(models.Model):
    vname = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now_add=True)
    isDelete = models.BooleanField(default=False)
    # 关联外键
    vusername = models.ForeignKey('User')
    vtempname = models.ForeignKey('Template')

    def __repr__(self):
        return self.vname