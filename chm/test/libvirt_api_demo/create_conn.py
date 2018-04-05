#!/bin/bash/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import libvirt

conn = libvirt.open('qemu:///system')
if conn is None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)
print('Create connection OK')
conn.close()
exit(0)
