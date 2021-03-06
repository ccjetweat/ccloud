import xml.etree.cElementTree as ET
import sys
from tools import Tool


class XMLTool(object):

    def __init__(self, xml_file):
        self.tree = ET.ElementTree(file=xml_file)

    def getTree(self):
        return self.tree

    def getRoot(self):
        return self.tree.getroot()

    def getIter(self, tag=None):
        return self.tree.iter(tag)

    def modifyElementText(self, elemType, textType, textValue):
        elems = self.getIter(elemType)
        for elem in elems:
            if elem.text == textType:
                elem.text = textValue
                break

    def modeifyElementAttrib(self, elemType, attribKey, attribType, attribValue):
        elems = self.getIter(elemType)
        for elem in elems:
            if elem.attrib[attribKey] == attribType:
                elem.attrib[attribKey] = attribValue
                break

    def writeToFile(self, file):
        self.tree.write(file, encoding='utf-8', xml_declaration=True)

    def writeToStdout(self):
        return self.tree.write(sys.stdout)


if __name__ == '__main__':
    # xmlObj = XMLTool(r'/root/KVM/test.xml')
    # tree = xmlObj.getTree()
    # root = xmlObj.getRoot()
    # print(root)
    # for root_child in root:
    #     print(root_child.tag, root_child.attrib)
    # for elem in xmlObj.getIter():
    #     print(elem.tag, elem.attrib)
    # names = xmlObj.getIter('currentMemory')
    # for name in names:
    #     print(name.text)
    #     if name.text == 'vm_name':
    #         name.text = 'centos'
    #         xmlObj.getTree().write(sys.stdout)
    # macs = xmlObj.getIter('mac')
    # for mac in macs:
    #     if mac.attrib['address'] == 'vm_mac':
    #         mac.attrib['address'] = '52:54:00:23:2e:4f'
    #         xmlObj.getTree().write(sys.stdout)
    #         # xmlObj.writeToFile('./demo.xml')
    #         break
    xmlTool = XMLTool(r'/root/KVM/centos7u4.xml')
    xmlTool.modifyElementText('name', 'vm_name', 'demo')
    xmlTool.modifyElementText('uuid', 'vm_uuid', Tool.createUUID('centos7.4'))
    xmlTool.modifyElementText('currentMemory', 'vm_mem', str(1024*1024))
    xmlTool.modeifyElementAttrib('vcpu', 'current', 'vm_cpus', '1')
    xmlTool.modeifyElementAttrib('source', 'file', 'vm_img', '/root/KVM/centos7u4.qcow2')
    xmlTool.modeifyElementAttrib('mac', 'address', 'vm_mac', Tool.randomMAC())
    # xmlTool.writeToStdout()
    xmlTool.writeToFile(r'/root/KVM/demo.xml')