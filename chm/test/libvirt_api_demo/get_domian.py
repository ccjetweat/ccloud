#!/bin/bash/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import libvirt
conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)

domainID = input("DomainID: ")
dom = conn.lookupByID(domainID)
if dom is None:
    print('Failed to get the domain object', file=sys.stderr)
else:
    print('Get domain object OK')
conn.close()
exit(0)

conn.close()
exit(0)