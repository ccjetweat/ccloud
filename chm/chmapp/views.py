#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from .models import User, Image, Template, Host, VM
from tools import Tool
import os
import commands
from libvirt_api import *

URL = 'qemu:///system'


# Create your views here.
# 登陆页面
def login(request):
    return render(request, 'chmapp/login.html')


# 验证信息
def auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.all()
        for user in users:
            if user.uname == username and user.upasswd == password:
                request.session['username'] = username
                user.isLogin = True
                user.save()
                # 逆向解析url
                return redirect(reverse('chmapp:user'))
        return redirect(reverse('chmapp:login'))


def getUserStatus(key):
    users = User.objects.filter(uname=key)
    for user in users:
        if user.isLogin:
            status = '在线'
        else:
            status = '离线'
    return status


# 跳转页面
def index(request):
    username = request.session.get("username", default='请登录')
    status = getUserStatus(username)
    return render(request, 'chmapp/index.html', {'username': username, 'status': status})


# 退出页面
def quite(request):
    username = request.session.get('username')
    user = User.objects.get(uname=username)
    user.isLogin = False
    user.save()
    logout(request)
    return redirect(reverse('chmapp:login'))


# 用户管理界面
def user(request):
    currentUser = request.session.get('username')
    status = getUserStatus(currentUser)
    if currentUser == 'admin':
        userList = User.objects.all().filter(isDelete=False)
    else:
        userList = User.objects.filter(uname=currentUser)
    return render(request, 'chmapp/userindex.html', {'username': currentUser, 'status': status, 'userList': userList})


# 添加用户
def useradd(request):
    if request.method == 'POST':
        currentName = request.session.get('username')
        status = getUserStatus(currentName)
        return render(request, 'chmapp/useradd.html', {'username': currentName, 'status': status})


# 修改用户
def usermod(request):
    currentName = request.session.get('username')
    status = getUserStatus(currentName)
    return render(request, 'chmapp/usermod.html', {'username': currentName, 'status': status})


# 删除用户
def userdel(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        user = User.objects.get(uname=username)
        if user is not None:
            user.isDelete = True
            user.save()
            return redirect(reverse('chmapp:user'))


# 保存用户
def usersave(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(uname=username)
            user.upasswd = request.POST.get('password')
            user.udesc = request.POST.get('description')
            user.save()
        except BaseException as e:
            newUser = User()
            newUser.uname = request.POST.get('username')
            newUser.upasswd = request.POST.get('password')
            newUser.udesc = request.POST.get('description')
            newUser.save()
        finally:
            return redirect(reverse('chmapp:user'))


# 镜像首页
def image(request):
    currentUser = request.session.get('username')
    status = getUserStatus(currentUser)
    imageList = Image.objects.all().filter(isDelete=False)
    return render(request, 'chmapp/imageindex.html', {'username': currentUser, 'status': status, 'imageList': imageList})


def imageadd(request):
    if request.method == 'POST':
        currentName = request.session.get('username')
        status = getUserStatus(currentName)
        return render(request, 'chmapp/imageadd.html', {'username': currentName, 'status': status})


def imagedel(request):
    if request.method == 'POST':
        image = Image.objects.get(iname=request.POST.get('imgname'))
        image.isDelete = True
        image.save()
        return redirect(reverse('chmapp:image'))


def imagesave(request):
    if request.method == 'POST':
        imageName = request.POST.get('imgname')
        imagePath = request.POST.get('imgpath')
        try:
            image = Image.objects.get(iname=imageName)
        except BaseException as e:
            newImage = Image()
            newImage.iname = imageName
            newImage.iaddr = imagePath
            srcPath = '/root/KVM/centos7u4.qcow2'
            newPath = os.path.join(imagePath, imageName)
            status, output = commands.getstatusoutput('qemu-img create -f qcow2 -b '+srcPath+' '+newPath)
            if status == 0:
                newImage.save()
        finally:
            return redirect(reverse('chmapp:image'))


# 模版管理界面
def template(request):
    currentUser = request.session.get('username')
    status = getUserStatus(currentUser)
    if currentUser == 'admin':
        tempList = Template.objects.all().filter(isDelete=False)
    else:
        tempList = Template.objects.filter(tname=currentUser).filter(isDelete=False)
    return render(request, 'chmapp/template.html', {'username': currentUser, 'status': status, 'tempList': tempList})


def tempadd(request):
    if request.method == 'POST':
        currentUser = request.session.get('username')
        status = getUserStatus(currentUser)
        imageList = Image.objects.all().filter(isDelete=False)
        return render(request, 'chmapp/tempadd.html', {'username': currentUser, 'status': status, 'imageList': imageList})


def tempmod(request):
    if request.method == 'POST':
        currentUser = request.session.get('username')
        status = getUserStatus(currentUser)
        tempObj = Template.objects.get(tname=request.POST.get('tempname'))
        imageList = Image.objects.all().filter(isDelete=False)
        return  render(request, 'chmapp/tempmod.html', {'username': currentUser, 'status': status, 'tempObj': tempObj, 'imageList': imageList})


def tempdel(request):
    if request.method == 'POST':
        temp = Template.objects.get(tname=request.POST.get('tempname'))
        temp.isDelete = True
        temp.save()
        return redirect(reverse('chmapp:template'))


def tempsave(request):
    if request.method == 'POST':
        tempName = request.POST.get('tempname')
        try:
            temp = Template.objects.get(tname=tempName)
            temp.tname = tempName
            temp.tcpus = int(request.POST.get('cpus'))
            temp.tmemory = int(request.POST.get('memory')) * 1024
            temp.tmac = Tool.randomMAC()
            image = Image.objects.get(iname=request.POST.get('imageSelect'))
            temp.timgName = image
            temp.save()
        except BaseException as e:
            newTemp = Template()
            newTemp.tname = request.POST.get('tempname')
            newTemp.tcpus = int(request.POST.get('cpus'))
            newTemp.tmemory = int(request.POST.get('memory')) * 1024
            newTemp.tmac = Tool.randomMAC()
            image = Image.objects.get(iname=request.POST.get('imageSelect'))
            newTemp.timgName = image
            newTemp.save()
        finally:
            return redirect(reverse('chmapp:template'))


def host(request):
    currentUser = request.session.get('username')
    status = getUserStatus(currentUser)
    if currentUser == 'admin':
        hostList = Host.objects.all().filter(isDelete=False)
    else:
        hostList = Host.objects.filter(belong=currentUser).filter(isDelete=False)
    return render(request, 'chmapp/hostindex.html', {'username': currentUser, 'status': status, 'hostList': hostList})


def vmadd(request):
    currentUser = request.session.get('username')
    status = getUserStatus(currentUser)
    tempList = Template.objects.all()
    return render(request, 'chmapp/vmadd.html', {'username': currentUser, 'status': status, 'tempList': tempList})


def vmdefine(request):
    currentUser = request.session.get('username')
    userObj = User.objects.get(uname=currentUser)
    if request.method == 'POST':
        appName = request.POST.get('appName')
        tempName = request.POST.get('tempName')
        tempObj = Template.objects.get(tname=tempName)
        imgObj = tempObj.timgName
        fxml = xmlConfig(tempObj, imgObj, appName)
        with open(fxml, 'rb') as fr:
            configXMLString = fr.read()
            if createVM(URL, configXMLString):
                newVM = VM()
                newVM.vname = appName + tempObj.tname
                newVM.vusername = userObj
                newVM.vtempname = tempObj
                newHost = Host()
                newHost.hname = appName + tempObj.tname
                newHost.hstatus = getVMStatus(URL, newHost.hname)
                newHost.haddr = '暂无'
                newHost.belong = userObj
                newVM.save()
                newHost.save()

        return redirect(reverse('chmapp:host'))


def open(request):
    if request.method == 'POST':
        hostname = request.POST.get('hostname')
        flag, status, addr = startVM(URL, hostname)
        if flag:
            hostObj = Host.objects.get(hname=hostname)
            hostObj.hstatus = status
            hostObj.haddr = addr
            hostObj.save()
            return redirect(reverse('chmapp:host'))


def shutdown(request):
    if request.method == 'POST':
        hostname = request.POST.get('hostname')
        flag, status = shutdownVM(URL, hostname)
        if flag:
            hostObj = Host.objects.get(hname=hostname)
            hostObj.hstatus = status
            hostObj.save()
            return redirect(reverse('chmapp:host'))

