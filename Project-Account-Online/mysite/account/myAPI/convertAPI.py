#-*-coding:utf-8-*- 支持中文 

import types 
# b转换为B KB MB函数   round( x [, n]  )方法返回浮点数x的四舍五入值  2017.2.11
#应用测试在： tests.py
def sizeConvert(b):
    if (type(b) is types.StringType): #是否string类型 
        b = int(b) if b.isdigit() else -1 #所有字符都是数字
    if b < 0:
        return 'err'
    elif 0 <= b < 1000:
        return '%i' % b + 'B'
    elif 1000 <= b < 1000000:
        return '%.2f' % round(float(b/1000.0),2) + 'KB' #保留2位小数,四舍五入
    elif 1000000 <= b < 1000000000:
        return '%.2f' % round(float(b/1000000.0),2) + 'MB'
    elif 1000000000 <= b < 1000000000000:
        return '%.2f' % round(float(b/1000000000.0),2) + 'GB'
    elif 1000000000000 <= b:
        return '%.2f' % round(float(b/1000000000000.0),2) + 'TB'


import unittest            
class TestconvertAPI(unittest.TestCase):
    def test_sizeConvert_0(self):
        size = 0
        self.assertEquals(sizeConvert(size),'0B')
    def test_sizeConvert_1(self):
        size = '999'
        self.assertEquals(sizeConvert(size),'999B')  
    def test_sizeConvert_2(self):
        size = 999
        self.assertEquals(sizeConvert(size),'999B')  
    def test_sizeConvert_3(self):
        size = '1a'
        self.assertEquals(sizeConvert(size),'err')  
    def test_sizeConvert_4(self):
        size = -9
        self.assertEquals(sizeConvert(size),'err')  
    def test_sizeConvert_5(self):
        size = 1995
        self.assertEquals(sizeConvert(size),'2.00KB')  
    def test_sizeConvert_6(self):
        size = 1006000
        self.assertEquals(sizeConvert(size),'1.01MB')  
    def test_sizeConvert_7(self):
        size = 1006000000
        self.assertEquals(sizeConvert(size),'1.01GB')  
    def test_sizeConvert_8(self):
        size = 1006000000000
        self.assertEquals(sizeConvert(size),'1.01TB')  



if __name__ == '__main__':
    unittest.main()