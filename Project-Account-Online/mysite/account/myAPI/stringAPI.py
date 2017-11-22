# -*- coding: utf-8 -*-  
#~  Filename:stringAPI.py  字符串类
'''
使用举例：
from myAPI import stringAPI 
if stringAPI.IsStrfindinput(sourcecode):   #有键盘输入 input 
'''

#"print  a23b\na34b\n    print abcd\n"   'print repr(  a23b)\na34b\n    print repr( abcd)\n\n' 2017.6.1
def printrepr(str):
    lists = str.split('\n')
    mylist = []
    for list in lists :
        list = list.rstrip() #删除右空白符（包括'\n', '\r',  '\t',  ' ')
        list = list.replace('print','print repr(') + ')\n' if 'print' in list else list + '\n'
        mylist.append(list)
    return ''.join(mylist)
#-------------------------------------------------------------------------------------------
# 功能：判断mystring中，有无含字符串'input'的行。有含字符串'input'的行返回：return True。 排除注释掉的字符串。
# mystring = " abc\ndef\n abc=input()\n#xy=input()zok  \n aaa\nbbbb"
# IsStrfindinput(mystring)     return True
#-------------------------------------------------------------------------------------------
def IsStrfindinput(mystring):
    lists=TxtStrToList(mystring)
    for ls in lists:
        inputbit=ls.find('input')#input位置
        tbit=ls.find('#')#注释位置
        if ((inputbit>0)&(tbit==-1))|((inputbit>0)&(inputbit<tbit)):
            return True
    return False
#-------------------------------------------------------------------------------------------
# 功能：在mystring字符串中，用\n分割，获得字符串列表。没有取消空行和注释行。
#    mystring = " abc\ndef\nxyzok  \n\n #hello  \n" #长度是5
#    liststr=[' abc', 'def', 'xyzok  ', '', ' #hello']
#-------------------------------------------------------------------------------------------
def TxtStrToList(mystring):
    mystring=mystring.rstrip()#删除右端的空格
    return mystring.split('\n')#字符串转换为列表
#-------------------------------------------------------------------------------------------
# 功能：在mystring字符串中，用\n分割，获得列表长度
# mystring = " abc\ndef\nxyzok  \n\n #hello  \n" #长度是5
#-------------------------------------------------------------------------------------------
def GetStringLineNum(mystring):
    lists=TxtStrToList(mystring)
    return len(lists)

#-------------------------------------------------------------------------------------------
# 功能：在mystring字符串中，获得首个特定字符串mystr='input('   行数、 行文本。排除注释行。
#    mystring = " abc\n#def=input()\nxyz\n  abc=input('in') "
#    n,strs=GetStrLine('input(',mystring)
#    n = 4   strs = "  abc=input('in')"
#-------------------------------------------------------------------------------------------
def GetStrLine(mystr,mystring):
    linebum=1 #从1开始
    liststr= TxtStrToList(mystring)
    for strs in liststr:
        if mystr in strs:
            s=strs.strip()#去掉前后空格''
            if s[:1]!='#':#判断第一个字符，排除注释行
                return linebum,strs
        linebum+=1
    return 0,''
#-------------------------------------------------------------------------------------------
# 功能：在mystr字符串中，获得开始空格
#    mystr = ' h    '
#    gNLUU=GetStrStartNULL(mystr)   ' '
#-------------------------------------------------------------------------------------------
def GetStrStartNULL(mystr):
    s=''
    for i in mystr:
        if i.isspace():#.isspace()的方法，判断是否是空格
            s+=' '#空格
        else:
            break #退出循环
    return s
#-------------------------------------------------------------------------------------------
# 功能：判断MyS字符串是否包含在MyStr字符串中
# MyS='F0'  IsListSubStr(MyList,MyStr)  True
# MyS='F1'  IsListSubStr(MyList,MyStr)  False
#-------------------------------------------------------------------------------------------
def IsStrSubString(MyS,MyStr):
    return False if MyStr.find(MyS)==-1 else True
#-------------------------------------------------------------------------------------------
# 功能：由lineNo行数获得一行文本
#     mystring=" abc\ndef\nxyz\n " #\n位置
#    GetStringLineTxt(2,mystring)
#    结果：def
#-------------------------------------------------------------------------------------------
def GetStringLineTxt(lineNo,mystring):
    listn=TxtStrToList(mystring)
    return listn[lineNo-1]

#-------------------------------------------------------------------------------------------
# 功能：获得特定字符串mystr='='前后的字符串,字符串分割。
#    mystring = " n1=int(raw_input('n1 = :\n'))"
#    txt1,txt2=GetStrTxt1Txt2('=',mystring)
#    txt1='n1='
#    txt2='int(raw_input('n1 = :\n'))'
#-------------------------------------------------------------------------------------------
def GetStrTxt1Txt2(mystr,mystring):
    pos = mystring.find(mystr)+1 #搜索第一个'='字符的位置
    if pos>0:
        return mystring[:pos],mystring[pos:]
    return '',''
#-------------------------------------------------------------------------------------------
# 功能：替换字符串为红色
# sourcestr='hello world good'
# q='world'
# repnewstr=repred(sourcestr,q) #   hello world(显示红色) good
#-------------------------------------------------------------------------------------------
#替换字符串为红色
def repred(sourcestr,q):
    rep ="<span style='color:red'>" +q+"</span>" #替换字符串显示红色
    repnewstr = sourcestr.replace(q,rep);
    return repnewstr


import unittest            
class TestStringAPI(unittest.TestCase):
    def test_printrepr(self):
        mystring = "print  a23b\na34b\n    print abcd\n"
        self.assertEquals(printrepr(mystring),'print repr(  a23b)\na34b\n    print repr( abcd)\n\n')  
    
    
    def test_TxtStrToList(self):
        mystring = " abc\ndef\nxyzok  \n\n #hello  \n" #长度是5
        self.assertEquals(TxtStrToList(mystring),[' abc', 'def', 'xyzok  ', '', ' #hello'])  

    def test_GetStringLineNum(self):
        mystring = " abc\ndef\nxyzok  \n\n #hello  \n" #长度是5
        self.assertEquals(GetStringLineNum(mystring),5) 
         
    def test_IsStrfindinput_1(self):
        mystring = " abc\ndef\n abc=input()\n#xy=input()zok  \n aaa\nbbbb"
        self.assertEquals(IsStrfindinput(mystring),True) 
    def test_IsStrfindinput_2(self):
        mystring = " abc\ndef\n abc='12'#input()\n#xy=input()zok  \n aaa\nbbbb"
        self.assertEquals(IsStrfindinput(mystring),False) 
    def test_IsStrfindinput_3(self):
        mystring = " abc\ndef\n abc='12'#\nxy=46  \n aaa\nbbbb"
        self.assertEquals(IsStrfindinput(mystring),False) 
    def test_IsStrfindinput_4(self):
        mystring = " abc\ndef\n abc=33\n#xy=input()zok  \n aaa\nbbbb"
        self.assertEquals(IsStrfindinput(mystring),False) 
    def test_IsStrfindinput_5(self):
        mystring = " abc\ndef\n abc=33\n xy=input()zok  #  \n aaa\nbbbb"
        self.assertEquals(IsStrfindinput(mystring),True) 

    def test_GetStrLine_1(self):
        mystring = " abc\n#def=input()\nxyz\n  abc=input('in') "
        self.assertEquals(GetStrLine("input(",mystring),(4, "  abc=input('in')")) 
    def test_GetStrLine_2(self):
        mystring = " abc\n#def=input()\nxyz\n  abc=inputw('in') "
        self.assertEquals(GetStrLine("input(",mystring),(0, "")) 

    def test_GetStrStartNULL_1(self):
        mystring = '  h    ' #空2格
        self.assertEquals(GetStrStartNULL(mystring), "  ") 
    def test_GetStrStartNULL_2(self):
        mystring = '  ' #空2格
        self.assertEquals(GetStrStartNULL(mystring), "  ") 
    def test_GetStrStartNULL_3(self):
        mystring = '' #空
        self.assertEquals(GetStrStartNULL(mystring), "") 

    def test_IsStrSubString_1(self):
        MyS,MyStr='F0','F06925EMS91.txt'
        self.assertEquals(IsStrSubString(MyS,MyStr), True) 
    def test_IsStrSubString_2(self):
        MyS,MyStr='F1','F06925EMS91.txt'
        self.assertEquals(IsStrSubString(MyS,MyStr), False) 
        
    def test_GetStringLineTxt(self):
        MyS,MyStr=2," abc\ndef\nxyz\n " #MyS  \n位置
        self.assertEquals(GetStringLineTxt(MyS,MyStr), "def") 
        
    def test_GetStrTxt1Txt2(self):        
        MyS,MyStr="="," n1=int(raw_input('n1 = :\n'))"
        self.assertEquals(GetStrTxt1Txt2(MyS,MyStr), (" n1=","int(raw_input('n1 = :\n'))")) 
        
        
                        
        
if __name__ == '__main__':
    unittest.main()