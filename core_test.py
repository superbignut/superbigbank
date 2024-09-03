from superbigcore import *
import json



class A:
    def init(self):
        print("yes")


if __name__ == '__main__':

    with open('snowball.json', 'r', encoding='utf8') as f:
        ret = json.load(f)

    a = A()
    a.init()
    print(ret)