#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import libvirt
from xml_tools import XMLTool
import os
import time

"""
libvirt.VIR_DOMAIN_NOSTATE      0
libvirt.VIR_DOMAIN_RUNNING      1
libvirt.VIR_DOMAIN_BLOCKED      2
libvirt.VIR_DOMAIN_PAUSED       3
libvirt.VIR_DOMAIN_SHUTDOWN     4
libvirt.VIR_DOMAIN_SHUTOFF      5
libvirt.VIR_DOMAIN_CRASHED      6
libvirt.VIR_DOMAIN_PMSUSPENDED  7
"""
src_xml_path = r'/root/KVM/centos7u4.xml'


def xmlConfig(template, image, appName):
    domName = appName + template.tname
    xmlTool = XMLTool(src_xml_path)
    xmlTool.modifyElementText('name', 'vm_name', domName)
    xmlTool.modifyElementText('uuid', 'vm_uuid', str(template.tuuid))
    print(template.tuuid)
    xmlTool.modifyElementText('currentMemory', 'vm_mem', str(template.tmemory*1024))
    xmlTool.modeifyElementAttrib('vcpu', 'current', 'vm_cpus', str(template.tcpus))
    imagePath = os.path.join(image.iaddr, image.iname)
    xmlTool.modeifyElementAttrib('source', 'file', 'vm_img', imagePath)
    xmlTool.modeifyElementAttrib('mac', 'address', 'vm_mac', template.tmac)

    xml_template_path = '/root/KVM/'+domName+'.xml'
    xmlTool.writeToFile(xml_template_path)
    return xml_template_path


def createVM(url, domainXMLString):
    try:
        conn = libvirt.open(url)
        if conn is None:
            flag = True
        else:
            flag = False
        dom = conn.defineXMLFlags(domainXMLString, 0)
        if dom is not None and dom.state()[0] == 5:
            flag = True
        else:
            flag = False
        # print(dom.state())
        # [5, 0]
        # 5 --> VIR_DOMAIN_SHUTOFF
    finally:
        conn.close()
        return flag


def startVM(url, domName):
    try:
        flag, status, addr = True, '', ''
        conn = libvirt.open(url)
        if conn is None:
            flag = False
        dom = conn.lookupByName(domName)
        if dom is None:
            flag = False
        # print(dom.state())   [5, 0]  VIR_DOMAIN_SHUTOFF_UNKNOWN
        # print(dom.state())   [5, 1]  VIR_DOMAIN_SHUTOFF_SHUTDOWN
        # print(dom.state())   [5, 2]  VIR_DOMAIN_SHUTOFF_DESTROYED
        if dom.state()[0] == libvirt.VIR_DOMAIN_SHUTOFF:
            if dom.create() >= 0:
                while dom.state()[0] != libvirt.VIR_DOMAIN_RUNNING:
                    continue
                status = '活动'
        else:
            flag = False

        time.sleep(8)
        ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
        for (name, value) in ifaces.iteritems():
            if value['addrs']:
                for ipaddr in value['addrs']:
                    if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4 and ipaddr['addr'] != '127.0.0.1':
                        addr = ipaddr['addr']

    finally:
        conn.close()
        return flag, status, addr


def shutdownVM(url, domName):
    try:
        flag, status = True, ''
        conn = libvirt.open(url)
        if conn is None:
            flag = False
        dom = conn.lookupByName(domName)
        if dom is None:
            flag = False

        if dom.state()[0] == libvirt.VIR_DOMAIN_RUNNING:
            if dom.shutdown() >= 0:
                time.sleep(5)
                while dom.state()[0] != libvirt.VIR_DOMAIN_SHUTOFF:
                    continue
                status = '关闭'
        else:
            flag = False

    finally:
        conn.close()
        return flag, status


def destroyVM(url, domName):
    try:
        conn = libvirt.open(url)
        if conn is None:
            print('连接创建失败')
        dom = conn.lookupByName(domName)
        if dom is None:
            print('获取域失败')
        print(dom.state())
        if dom.destroy() < 0:
            print('强制关闭客户机失败')
    finally:
        conn.close()


def removeVM(url, domName):
    try:
        conn = libvirt.open(url)
        if conn is None:
            print('连接创建失败')
        dom = conn.lookupByName(domName)
        if dom is None:
            print('获取域失败')
        state, reason = dom.state()
        if state == libvirt.VIR_DOMAIN_RUNNING:
            print('虚拟机正在运行')
        else:
            dom.undefineFlags(0)
    finally:
        conn.close()


if __name__ == '__main__':
    URL = 'qemu:///system'
    # with open('/root/KVM/demo.xml', 'rb') as f:
    #     domainXMLString = f.read()
    # createVM(url, domainXMLString)
    # startVM(url, 'demo')
    # shutdownVM(url, 'demo')
    # destroyVM(url, 'demo')
    # removeVM(url, 'demo')
    # ipaddr = getInterfaceAddress(url, 'demo')
    # print(ipaddr)
    hostname = 'nginxcentos7'
    conn = libvirt.open(URL)
    dom = conn.lookupByName(hostname)
    print(dom.state()[0])
