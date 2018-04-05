import commands
# print(commands.getoutput('ls /'))
# status, output = commands.getstatusoutput('ls /')
status, output = commands.getstatusoutput('qemu-img create -f qcow2 -b /root/KVM/centos7u4.qcow2 /root/KVM/centos7.qcow2')
print(type(status))