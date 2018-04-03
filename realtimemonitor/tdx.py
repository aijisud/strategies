# -*- coding: utf-8 -*-

from pytdx.hq import TdxHq_API


if __name__ == '__main__':

    api = TdxHq_API()
    api.connect()
    a = api.get_security_list(1, 0)
    b = api.get_security_list(0, 0)
    print(a)
    print(len(a))
    #print(b)

#end
