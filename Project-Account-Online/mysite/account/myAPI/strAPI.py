# -*- coding: utf-8 -*-
'''
使用举例：
from myAPI.strAPI import strAPI
if strAPI('in input').isStr('input'): True

Created on 2017-05-29
'''
from myFile import GetTxtfile
class strAPI:
    def __init__(self, str):
        self.str = str
    
    def isStr(self,MyStr):
        return False if self.str.find(MyStr) == -1 else True#(strAPI('hello world!').isStr('hello w'),True) 
    
    def isList(self,MyList):
        return any([i == self.str for i in MyList])#(strAPI('hellow').isList(['hello','world']),False)    
        return any([i in self.str for i in MyList])#(strAPI('hellow').isList(['hello','world']),True)         
    
    def getStr1Str2(self,s):#strAPI('helloworld!').getStr1Str2('o'),('hello', 'world!')
        pos = self.str.find(s)+1 #搜索第一个s字符串的位置
        if pos>0:
            return self.str[:pos],self.str[pos:]
        return '',''

import unittest            
class TeststrAPI(unittest.TestCase):
    def test_isStr1(self):
        self.assertEquals(strAPI('hello world!').isStr('hello w'),True)          
    def test_isStr2(self):
        self.assertEquals(strAPI('helloworld!').isStr(''),True) 
    def test_isStr3(self):
        self.assertEquals(strAPI('helloworld!').isStr(' '),False) 
                 

    def test_isList1(self):
        self.assertEquals(strAPI('hello').isList(['hello','world']),True)          
    def test_isList2(self):
        self.assertEquals(strAPI('hellow').isList(['hello','world']),False)          
    def test_isList3(self):
        self.assertEquals(strAPI('hell').isList(['hello','world']),False)          

    def test_getStr1Str2(self):
        self.assertEquals(strAPI('helloworld!').getStr1Str2('o'),('hello', 'world!'))          

# txtfile文本文件，代码区用<code> </code>标识 2017.6.14
def txt_replace_html(txtfile):
    txt = GetTxtfile(txtfile)
    strlist = txt.split("\n")
    txt = ''
    for s in strlist: 
        s = s.rstrip()# 去掉<code>后面的不可见字符
        txt += s if ("<code>" in s) or ("</code>" in s) else s + '<br>'
    txt = txt.replace("<code>", "<pre><code>") # 加代码标志
    txt = txt.replace("</code>", "</code></pre>")    
    txt = txt.replace(">>> ", '<span class="prompt">>>> </span>')  # >>>显示桔红色                            
    txt = txt.replace("(", "(<span class='string'>") # ( )内部显示红色 
    txt = txt.replace(")", "</span>)")
    txt = txt.replace("[", "[<span class='string'>") # [ ]内部显示红色 
    txt = txt.replace("]", "</span>]")       
    txt = txt.replace("{", "{<span class='string'>") # { } 内部显示红色 
    txt = txt.replace("}", "</span>}") 
    return txt 

def txt_replace_html_xmp(txtfile):
    txt = GetTxtfile(txtfile)
    strlist = txt.split("\n")
    txt = ''
    for s in strlist: 
        s = s.rstrip()# 去掉<code>后面的不可见字符
        txt += s  if ("<code>" in s) or ("</code>" in s) else s + '\n'
    txt = txt.replace("<code>", "<pre><code><xmp>") # 加代码标志
    txt = txt.replace("</code>", "</xmp></code></pre>")
    return txt
 
# txtfile文本文件，代码区用<code> </code>标识；黑色代码区用code_start codeend标识；‘>试’中间无空格  2017.6.17
# mystr=javascript 适合函数代码；mystr=css适合css body代码；mystr=markup适合html代码
def txt_to_html(txtfile,mystr):
    txt = GetTxtfile(txtfile)
    strlist = txt.split("code_")
    txt,txt1,txt2 = '','',''
    for s in strlist:
        s = s.replace('<', '&lt')
        s = s.replace('>', '&gt')
            
        s = s.replace('&lta', '<a')
        s = s.replace(u'&gt试', u'>试')
        s = s.replace('&lt/a&gt', '</a>')
        if 'start' not in s: #处理 <code> </code>区域；        
            s = s.replace('&ltcode&gt', '<pre><code>')
            s = s.replace('&lt/code&gt', '</code></pre>') 
            txt1 +=  s.replace('\n', '<br>')
            
        else: #处理 code_start codeend区域；
            slist = s.split("codeend")
            slist[0] = slist[0].replace('start\n', '')      
            #s = '<pre><code  class="language-javascript">' +slist[0] + '</code></pre>'
            s = '<pre><code  class="language-' + mystr + '">' +slist[0] + '</code></pre>'
            slist[1] = slist[1].replace('&ltcode&gt', '<pre><code>')
            slist[1] = slist[1].replace('&lt/code&gt', '</code></pre>') 
            s += slist[1].replace('\n', '<br>')
            txt += s
    txt2 = txt1+txt
    txt2 = txt2.replace("[", "[<span class='string'>") # [ ]内部显示红色 
    txt2 = txt2.replace("]", "</span>]")       
    txt2 = txt2.replace("{", "{<span class='string'>") # { } 内部显示红色 
    txt2 = txt2.replace("}", "</span>}") 
    txt2 = txt2.replace("(", "(<span class='string'>") # ( )内部显示红色 
    txt2 = txt2.replace(")", "</span>)")    
    return txt2 



if __name__ == '__main__':
    unittest.main()