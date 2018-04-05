import xml.etree.cElementTree as ET
import sys


class XML(object):

    def __init__(self, xml_file):
        self.tree = ET.ElementTree(file=xml_file)

    def getTree(self):
        return self.tree

    def getRoot(self):
        return self.tree.getroot()

    def getIter(self, tag=None):
        return self.tree.iter(tag)

    def writeToFile(self, file):
        self.tree.write(file, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    xmlObj = XML(r'/root/KVM/test.xml')
    tree = xmlObj.getTree()
    root = xmlObj.getRoot()
    # print(root)
    # for root_child in root:
    #     print(root_child.tag, root_child.attrib)
    # for elem in xmlObj.getIter():
    #     print(elem.tag, elem.attrib)
    # names = xmlObj.getIter('name')
    # for name in names:
    #     if name.text == 'vm_name':
    #         name.text = 'centos'
    #         xmlObj.getTree().write(sys.stdout)
    macs = xmlObj.getIter('mac')
    for mac in macs:
        if mac.attrib['address'] == 'vm_mac':
            mac.attrib['address'] = '52:54:00:23:2e:4f'
            # xmlObj.getTree().write(sys.stdout)
            xmlObj.writeToFile('./demo.xml')
            break

