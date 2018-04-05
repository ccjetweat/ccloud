#!/bin/bash/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import libvirt
conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)

domainName = 'nginx-1'
dom = conn.lookupByName(domainName)
if dom is None:
    print('Failed to get the domain object', file=sys.stderr)
else:
    print('Get domain object OK')
id = dom.ID()
uuid = dom.UUIDString()
os_type = dom.OSType()
print(id, uuid, os_type)
# hostname = dom.hostname()
# print(hostname)
conn.close()
exit(0)

conn.close()
exit(0)