# -*- coding: utf-8 -*-
'''
   ListDictAPI.py 列表字典类
   
2017.1.16
'''
import json
import jieba  #中文分词

#由整数产生列表
def IntegerToList(num):
    return [num+1 for num in range(num)]    
class listdictAPI:
    def __init__(self, myList, myStr):
        self.subStrList = myList
        self.inputStr = myStr


    #判断列表MyList中所有元素,是否都包含在字符串MyStr中。是True、否False
    def isListAllInStr(self):
        return all([i in self.inputStr for i in self.subStrList])

        
    #判断列表MyList中的一个（含）以上元素是否包含在字符串MyStr中。是True、否False
    def isStrHasSubList(self):
        '''
        >>> any(['a', 'b', 'c', 'd'])  #列表list，元素都不为空或0
        True
        >>> any(['a', 'b', '', 'd'])  #列表list，存在一个为空的元素
        True
        >>> any([0, '', False])  #列表list,元素全为0,'',false
        False
        '''
        return any([i in self.inputStr for i in self.subStrList])
    
    #判断字符串MyStr是否包含在列表MyList中。是True、否False
    def isStrInList(self):
        return any([self.inputStr in i for i in self.subStrList])

# 列表字典去重[{'a':1},{'b':2},{'a':1},{'b':2},1,'1']  ['1', 1, {'b': 2}, {'a': 1}] 
def listdictSet(listdict):
    mylist = []
    mynewlist = []
    for d in listdict: # d字典转换为字符串str(d);将列表字典元素转换为列表字符串元素
        mylist.append(d) if isinstance(d,int) else mylist.append(str(d))    
        mylist =list(set(mylist))
    for s in mylist: # s字符串转换为字典eval(s);将列表字符串元素转换为列表字典元素
        mynewlist.append(s) if isinstance(s,int) else mynewlist.append(s) if isinstance(eval(s),int) else mynewlist.append(eval(s))
    return mynewlist


    
#两个列表相加，返回列表 (['a','b'],['1','2']),  ['a','b','1','2']      
def listAdd(list1, list2):
    return list1 + list2

#两个列表字典相加（没有key键名去重复功能），返回列表字典
def listdictAdd(listdict1,listdict2):
    return listdict1+listdict2

#listdict列表字典按某一键名key的值相同去重复
def listdictDelRepeatkey(listdict,key):
    newlistdict=[]
    newlistdict.append(listdict[0])
    for dict in listdict:
        k=0
        for item in newlistdict:
            if dict[key] != item[key]:k+=1
            else: break
            if k == len(newlistdict): newlistdict.append(dict)
    return newlistdict

# 从obj对象中，获得包含str字符串在内的新对象。
# 例：(['1.txt','2.txt','hello','book.json'],'.txt'),['1.txt','2.txt'])
# obj对象是字符串返回字符串、元组返回元组、列表返回列表；obj对象是字典，只获得键名，返回列表。
def getObjContainStr(obj,str):
    return filter(lambda x: str in x ,obj) 

# 将列表中的字符串(字符串格式 '/3_HTML')，转化为二元元组:格式 ('3','HTML')，返回列表元组。
def getListTuple(MyList):
    import re
    reCmp = re.compile('([^/]+)_([^/]+)$')
    return  [reCmp.search(i).groups() for i in MyList] 

#从列表myList中，按照q中文分词，搜索出符合条件的newList列表
#myList =['中国人民','人民万岁']是Python字符串列表，而myList =[u'中国人民',u'人民万岁'] Unicode !!! 
def searchList(myList,q):
    newList = []
    qlists =list(jieba.cut(q, cut_all = True)) #q中文分词
    for qs in qlists:
        newList += [u for u in myList  if qs in u.split('/')[-1]]# myList =[u'中国人民',u'人民万岁'] Unicode
        #newList += [u for u in myList  if qs in u.split('/')[-1].decode('UTF-8')]#将Python字符串转换成Unicode
    newList = list(set(newList)) #去掉重复元素  
    return newList 


import unittest            
class TestlistdictAPI(unittest.TestCase):
    def test_IntegerToList(self):
        num = 4
        self.assertEquals(IntegerToList(num),[1,2,3,4])  
    
    
  
    def test_isListAllInStr_all_T(self):
        listdictapi=listdictAPI(['F','EMS','txt'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isListAllInStr(),True)                                           
    def test_isListAllInStr_1_F (self):
        listdictapi=listdictAPI(['F1','EMS','txt'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isListAllInStr(),False)                                           
    def test_isListAllInStr_2_F (self):
        listdictapi=listdictAPI(['F1','EMS1','txt'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isListAllInStr(),False)                                           
    def test_isListAllInStr_3_F(self):
        listdictapi=listdictAPI(['F1','EMS1','txt1'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isListAllInStr(),False)                                           
 
    def test_isListAInStr_1_T (self):
        listdictapi=listdictAPI(['F','EMS1','txt1'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isStrHasSubList(),True)                                           
    def test_isListAInStr_2_T (self):
        listdictapi=listdictAPI(['F','EMS','txt1'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isStrHasSubList(),True)                                           
    def test_isListAInStr_3_T (self):
        listdictapi=listdictAPI(['F','EMS','txt'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isStrHasSubList(),True)                                           
    def test_isListAInStr_all_F(self):
        listdictapi=listdictAPI(['F1','EMS1','txt1'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isStrHasSubList(),False)  
        
    def test_isStrInList_T (self):
        listdictapi=listdictAPI(['F','EMS','txt'],'M')
        self.assertEquals(listdictapi.isStrInList(),True)                                           
    def test_isStrInList_F(self):
        listdictapi=listdictAPI(['F1','EMS1','txt1'],'1t')
        self.assertEquals(listdictapi.isStrInList(),False)  
     
    def test_listdictSet(self):
        self.assertEquals(listdictSet([{'a':1},{'b':2},{'a':1},{'b':2},1,'1']),
                          ['1', 1, {'b': 2}, {'a': 1}])
        
    
    def test_listAdd(self):
        self.assertEquals(listAdd(['a','b'],['1','2']),['a','b','1','2'] )       
    def test_listdictAdd(self):        
        self.assertEquals(listdictAdd([{'a':1,'b':2},{'c':3,'d':4}],
                                      [{'e':5,'f':6,},{'g':7,'a':8}]),
                    [{'a':1,'b':2},{'c':3,'d':4},{'e':5,'f':6,},{'g':7,'a':8}])  

    def test_listdictDelRepeatkey(self):
        listdict=[{'host':'c21', 'cpu':1},{'host':'c21', 'cpu':2},
                  {'host':'c22', 'cpu':3},{'host':'c23', 'cpu':4},
                  {'host':'c22', 'cpu':5},{'host':'c23', 'cpu':6},
                  {'host':'c24', 'cpu':7}]
        self.assertEquals(listdictDelRepeatkey(listdict,'host'),
                        [{'host': 'c21', 'cpu': 1}, {'host': 'c22', 'cpu': 3},
                         {'host': 'c23', 'cpu': 4}, {'host': 'c24', 'cpu': 7}])
                                                                    
    def test_getObjContainStr_null(self):
        self.assertEquals(getObjContainStr('abcd','x'),'')                                           
    def test_getObjContainStr_str(self):
        self.assertEquals(getObjContainStr('abcd','a'),'a')
    def test_getObjContainStr_tuple(self):
        self.assertEquals(getObjContainStr(('1.txt','2.txt','hello','book.json'),
                        '.'),('1.txt','2.txt','book.json'))
    def test_getObjContainStr_list(self):
        self.assertEquals(getObjContainStr(['1.txt','2.txt','hello','book.json'],
                        '.txt'),['1.txt','2.txt'])
    def test_getObjContainStr_dict(self):
        self.assertEquals(getObjContainStr({'abcd':'1.txt','cd':'2.txt',
                        'defg':'b.js'},'cd'),['abcd', 'cd'])
        
    def test_getListTuple(self): 
        self.assertEquals(getListTuple(['.../1_python', '.../2_django',
            '.../3_HTML']),[('1', 'python'), ('2', 'django'), ('3', 'HTML')])

    def test_searchList_1(self):
        myList =['.../1_python', '.../2_django']
        q='python_'
        self.assertEquals(searchList(myList,q),['.../2_django', '.../1_python'])

    def test_searchList_2(self):
        myList =['1_python', '2_django']
        q='python_'
        self.assertEquals(searchList(myList,q),['1_python', '2_django'])
        
    def test_searchList_3(self):
        myList =[u'中国人民',u'人民万岁']
        q = u'人民'
        self.assertEquals(searchList(myList,q),[u'\u4e2d\u56fd\u4eba\u6c11', u'\u4eba\u6c11\u4e07\u5c81'])

if __name__ == '__main__':
    unittest.main()


#------------------------------------------------------------------------
#替换字符串为红色
def repred(sourcestr,q):
    rep ="<span style='color:red'>" +q+"</span>" #替换字符串显示红色
    return sourcestr.replace(q,rep)
#------------------------------------------------------------------------
# 函数: def listdictRepQRed(ListDict,keyname,Q):
# 功能：将列表含字典键值keyname='fname' 短文件名中，Q（字符串）替换显示为红色
# 输入：ListDict 列表含字典，键值keyname='fname' ，Q（字符串）替换显示为红色
# 输出：返回替换后的字符串
# 版本：ver2.1
# 作者：吴春龙    时间：2016.7.5
# 测试环境：python2.7
#    Q=u'测试' #测试显示为红色
#    Lists=[{'fname':u'py测试.py','txt':'hello'},{'fname':1,'txt':'world'}]
#    mynewlist=listdictRepQRed(request,Lists,'fname',q)
#    return render_to_response('test.html',{'gFileLists':mynewlist})
#    {% for gFileList in gFileLists %}
#      {{ gFileList.fname|safe  }} </br> 模板中关转义
#    {% endfor %}
#------------------------------------------------------------------------
def listdictRepQRed(ListDict,keyname,Q):
    for slist in ListDict:
        n=0
        for key in slist.keys(): #字典键值
            dactval=slist.values()[n]
            if isinstance(dactval, int):#判断是否为整型
                dactval=str(dactval)
            if (key==keyname): #只替换fname一个键值
                dactval=repred(dactval,Q)
                slist[key]=dactval  #替换字典值
            n+=1
    return ListDict
#------------------------------------------------------------------------
# 函数: def listdictRepQlistRed(request,ListDict,keyname,Q):
# 功能：将列表含字典键值fname短文件名中，Q（字符串）中文分词 替换显示为红色。
# 输入：ListDict 列表含字典，键值keyname='fname' ，Q（字符串）替换显示为红色
# 输出：返回替换后的字符串
# 版本：ver2.1
# 作者：吴春龙    时间：2016.7.5
# 测试环境：python2.7
#    Q=u'测py' #测试显示为红色
#    Lists=[{'fname':u'py测试.py','txt':'hello'},{'fname':1,'txt':'world'}]
#    mynewlist=listdictRepQlistRed(Lists,'fname',Q)
#    return render_to_response('test.html',{'gFileLists':mynewlist})
#
#    {% for gFileList in gFileLists %}
#      {{ gFileList.fname|safe  }} </br> 模板中关转义
#    {% endfor %}
#------------------------------------------------------------------------
def listdictRepQlistRed(ListDict,keyname,Q):
    qlists =list(jieba.cut(Q, cut_all = True)) #Q中文分词
    for qs in qlists:
        ListDict=listdictRepQRed(ListDict,keyname,qs)
    return ListDict

# listdict列表字典按某一键名key的值相同去重复, 两种实现方式比较：
# import time
# import copy
# listdict = [{'a':12,'b':21},{'a':13,'b':22},{'a':14,'b':22},
#      {'a':15,'b':23},{'a':16,'b':22}]
# def listdictDelRepeatkey(listdict,key):
#     d = {}
#     for i in listdict:
#         d.setdefault(i[key], 0)
#         d[i[key]] += 1
#         at = copy.copy(listdict)
#     for i in at:
#         if d[i[key]] > 1:
#             listdict.remove(i)
#     return listdict
# 
# def listdictDelRepeatkey1(listdict,key):
#     newlistdict=[]
#     newlistdict.append(listdict[0])
#     for dict in listdict:
#         k=0
#         for item in newlistdict:
#             if dict[key] != item[key]:k+=1
#             else: break
#             if k == len(newlistdict): newlistdict.append(dict)
#     return newlistdict
# 
# start = time.time()
# print listdictDelRepeatkey(listdict,'b')
# end = time.time()
# print end-start
# 
# start = time.time()
# print listdictDelRepeatkey1(listdict,'b')
# end = time.time()
# print end-start
# 
# '''
# 测试结果
# [{'a': 12, 'b': 21}, {'a': 15, 'b': 23}]
# 6.50882720947e-05
# [{'a': 12, 'b': 21}, {'a': 15, 'b': 23}]
# 2.09808349609e-05'''
