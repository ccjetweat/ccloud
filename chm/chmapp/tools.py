import random
import uuid


class Tool(object):

    @staticmethod
    def uuid_hex():
        return uuid.uuid1()

    @staticmethod
    def randomMAC():
        mac = [0x52, 0x54, 0x00,
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0xff),
               random.randint(0x00, 0xff)]
        return ':'.join(map(lambda x: "%02x" % x, mac))

    @staticmethod
    def copyFile(src, dest):
        try:
            fr = open(src, 'rb')
            fw = open(dest, 'wb')
            while True:
                data = fr.read(1024)
                if data:
                    fw.write(data)
                else:
                    flag = True
                    break
            return flag
        except IOError:
            flag = False
            return flag
        finally:
            fr.close()
            fw.close()


if __name__ == '__main__':
    tool = Tool()
    # while True:
    #     name = input("pleace input a name: ")
    #     uuid_string = tool.createUUID(name)
    #     print(uuid_string)
    #     print(type(uuid_string))
    #     if name == 'quit':
    #         break

    # src = r'/root/KVM/centos7u4.xml'
    # dest = os.path.join('/root/KVM', 'test.xml')
    # if tool.copyFile(src, dest):
    #     print('OK')
    mac = tool.randomMAC()
    print(Tool.uuid_hex())
