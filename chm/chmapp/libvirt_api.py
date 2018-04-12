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
    domName = appName + '-' + template.tname
    xmlTool = XMLTool(src_xml_path)
    xmlTool.modifyElementText('name', 'vm_name', domName)
    xmlTool.modifyElementText('uuid', 'vm_uuid', str(template.tuuid))
    xmlTool.modifyElementText('currentMemory', 'vm_mem', str(template.tmemory*1024))
    xmlTool.modeifyElementAttrib('vcpu', 'current', 'vm_cpus', str(template.tcpus))
    imagePath = os.path.join(image.iaddr, image.iname)
    xmlTool.modeifyElementAttrib('source', 'file', 'vm_img', imagePath)
    xmlTool.modeifyElementAttrib('mac', 'address', 'vm_mac', template.tmac)

    xml_template_path = '/root/KVM/'+domName+'.xml'
    xmlTool.writeToFile(xml_template_path)
    return xml_template_path, domName


def createVM(url, domainXMLString):
    flag, info = True, 'OK'
    try:
        conn = libvirt.open(url)
        if conn is None:
            flag = False
        dom = conn.defineXMLFlags(domainXMLString, 0)
        if dom is None:
            flag = False
        if dom.state()[0] != libvirt.VIR_DOMAIN_SHUTOFF:
            flag = False
    except libvirt.libvirtError as vm_error:
        info = str(vm_error)
        flag = False

    finally:
        conn.close()
        return flag, info


def startVM(url, domName):
    flag, status, address, info = True, '', '', 'OK'
    try:
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
            dom.create()
            time.sleep(12)

        if dom.state()[0] == libvirt.VIR_DOMAIN_RUNNING:
            status = '活动'

        ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
        for (name, value) in ifaces.iteritems():
            if value['addrs']:
                for ipaddr in value['addrs']:
                    if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4 and ipaddr['addr'] != '127.0.0.1':
                        address = ipaddr['addr']

    except libvirt.libvirtError as vm_error:
        info = str(vm_error)
        flag = False

    finally:
        conn.close()
        return flag, status, address, info


def shutdownVM(url, domName):
    flag, status, info = True, '', 'OK'
    try:
        conn = libvirt.open(url)
        if conn is None:
            flag = False
        dom = conn.lookupByName(domName)
        if dom is None:
            flag = False

        if dom.state()[0] == libvirt.VIR_DOMAIN_RUNNING:
            dom.shutdown()
            time.sleep(8)

        if dom.state()[0] == libvirt.VIR_DOMAIN_SHUTOFF:
            status = '关闭'

    except libvirt.libvirtError as vm_error:
        info = str(vm_error)
        flag = False

    finally:
        conn.close()
        return flag, status, info


def destroyVM(url, domName):
    flag, status, info = True, '', 'OK'
    try:
        conn = libvirt.open(url)
        if conn is None:
            flag = False
        dom = conn.lookupByName(domName)
        if dom is None:
            flag = False

        if dom.state()[0] == libvirt.VIR_DOMAIN_RUNNING:
            dom.destroy()
            time.sleep(2)

        if dom.state()[0] == libvirt.VIR_DOMAIN_SHUTOFF:
            status = '关闭'

    except libvirt.libvirtError as vm_error:
        info = str(vm_error)
        flag = False

    finally:
        conn.close()
        return flag, status, info


def removeVM(url, domName):
    flag, info = True, 'OK'
    try:
        conn = libvirt.open(url)
        if conn is None:
            flag = False
        dom = conn.lookupByName(domName)
        if dom is None:
            flag = False

        if dom.state()[0] == libvirt.VIR_DOMAIN_SHUTOFF:
            dom.undefineFlags(0)
        else:
            flag = False
            info = 'The guest host is running'

    except libvirt.libvirtError as vm_error:
        info = str(vm_error)
        flag = False

    finally:
        conn.close()
        return flag, info


if __name__ == '__main__':
    URL = 'qemu:///system'
    conn = libvirt.open(URL)
    dom = conn.lookupByName('mysql-centos7')
    # vmInfo = startVM(URL, 'mysql-centos7')
    # vmInfo = shutdownVM(URL, 'mysql-centos7')
    # vmInfo = destroyVM(URL, 'mysql-centos7')
    # vmInfo = removeVM(URL, 'mysql-centos7')
    # print(vmInfo)
    # ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
    # for (name, value) in ifaces.iteritems():
    #     if value['addrs']:
    #         for ipaddr in value['addrs']:
    #             if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4 and ipaddr['addr'] != '127.0.0.1':
    #                 print(ipaddr['addr'])
    # print(dom.state()[0])
    conn.close()
