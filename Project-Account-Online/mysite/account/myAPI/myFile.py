# -*- coding: utf-8 -*-
from __future__ import unicode_literals #将类似 str = "测试2--test2" 转换成unicode ？
import os
import os.path

from listdictAPI import  listdictAPI,searchList
from pageAPI import Page,_get_model_by_page #工程中使用的类

import unittest
'''
myFile.py   文件类

1、单元测试，难道只支持相对目录和绝对目录？
相对目录: dir = 'testMyFile'
绝对目录：dir = '/Users/wuchunlong/local/flask/abbyBlog-0001/edustack/upvideo'

2、工程文件（例如：video.py def test_toFileNameListDicts() ），支持如下绝对目录
绝对目录：dir = 'edustack/static/oday/video/0_flask'
'''
import re
import json
def isJsonable(obj):
    try:
        json.dumps(obj)
    except:
        return False
    else:
        return True

def toDict(model):
    if not hasattr(model, "__dict__"):
        return {}
    retDict = {k:v for k,v in model.__dict__.items() if isJsonable(v)}
    jsonDict = getattr(model, "_jsonMapDict", {})
    for (key,fun) in jsonDict.items():
        if hasattr(model, key):
            field = getattr(model, key)
            retDict[key] = fun(field)
    return retDict

class MyFile:
    def __init__(self, dirpath, strlist):#strlist ＝［］获得指定目录下,全部目录名、文件名
        self.dirPath = dirpath #目录路径 dirpath = '.../edustack/upvideo/testMyFile'
        self.strList = strlist #指定类型的文件名列表strlist = ［'.txt'］获得全部.txt文件名
        
    #以列表形式，获得指定目录下，指定类型的全部文件名。strlist ＝［］获得指定目录下,全部目录名、文件名.    
    def toNameList(self):
        try:
            # 列表形式，返回指定目录下所有的文件和目录名（不含路径的短文件名）
            fileNames = os.listdir(self.dirPath)       
        except Exception as ex:
            #print "toNameList() err!"
            #raise
            return "toNameList() err! " + str(ex)        
        if (len(self.strList) > 0):
            fileNames = [fileName for fileName in fileNames 
                        if listdictAPI(self.strList, fileName).isStrHasSubList()]
        fileList = [os.path.join(self.dirPath, i) for i in fileNames 
                    if (not '._' in i)&(not '.DS' in i)]#（含路径的文件名）2016.10.24
        
        return fileList
    
    #以列表形式，获得指定目录下，全部目录名。目录名不能含有‘.’ ，默认设定：strlist＝［］   
    def toDirList(self):
        return [i for i in self.toNameList() if '.' not in i]
        
    #以列表字典形式，获得指定目录下指定类型的全部含路径文件名
    #[{'filename':'/static/1.mp4'}，{'filename':'/static/2.mp4'}，...] 
    def toFileNameListDict(self):
        filenames = self.toNameList()        
        return [{'filename':filename[filename.find('/',0):]} 
                for filename in filenames]
        
    #以列表字典形式，获得指定目录下，指定类型的全部含路径文件名和不含路径文件名 
    #[{'filename':'/static/1.mp4','fname':'1.mp4'}，{'filename':'/static/2.mp4','fname':'2.mp4'}，...] 
    def toFileNameFNameListDict(self):
        filenames = self.toNameList()
        return [{'filename':filename[filename.find('/',0):].decode('UTF-8'),
                 "fname":filename.split('/')[-1].decode('UTF-8')} 
                for filename in filenames]
    #以列表字典形式，获得指定目录下,所有二级目录，指定类型的全部含路径文件名和不含路径文件名 2016.10.24
    def toDirDownFileNameFNameListDict(self,myStr): #指定类型myStr='.py'
        FileNameList = []
        dirList = self.toDirList()
        for dir in dirList:
            NameList = MyFile(dir+'/',[myStr]).toFileNameFNameListDict()
            for Name in NameList:
                FileNameList.append(Name)
        return FileNameList
    
    #以列表形式，获得指定目录下,所有二级目录，指定类型的全部含路径文件名
    #["edustack/static/oday/video/0_flask/1_Flask.mp4", "edustack/static/oday/video/0_flask/3_flaskMySQL.mp4"]
    def toDirDownFileNameList(self,myStr): #指定类型myStr='.py'
        FileNameList = []
        dirList = self.toDirList()
        for dir in dirList:
            NameList = MyFile(dir+'/',[myStr]).toNameList()
            for Name in NameList:
                FileNameList.append(Name)
        return FileNameList
            
    #以元组形式，获得指定目录下不含路径的[(编号(myid),目录名(Dir))]。
    #例如：['.../1_python', '.../2_django']   [('1','python'),('2','django')]     
    
    def toIdDirListTuple(self):
        try:
            reCmp = re.compile('/(\d+)_([^/]+)$')
            aList = [reCmp.search(i).groups() for i in self.toDirList()]
            return aList
        except Exception as e:
            return  "toIdDirListTuple() err! " + str(e)
    
    #以列表字典形式，获得指定目录下json文件名，读json文件格式数据(列表字典)。
    def toReadJson(self):
        nameLists = self.toNameList()
        return [readJson(nameList) for nameList in nameLists]
    
    #以列表字典形式，将指定目录下json文件名，做为字典键值，键名：name  
    #例： .../博客名1.json .../博客名2.json [{'name':'博客名1'},{'name':'博客名2'}]
    def toJsonNameListDict(self):
        nameLists = self.toNameList()
        return [{'name':nameList.split('/')[-1][:-5].decode('UTF-8')} #-5 <-->.json
                for nameList in nameLists]
        
    #以列表字典形式，获得指定目录下json文件名、文件内容。两个列表字典字段相加。
    #例：[{'name':'博客名1','sgx':30}] + [{'file':'1.txt','num':10}] =
    #   [{'name':'博客名1','sgx':30,'file':'1.txt','num':10}] 
    def toJsonListDict(self):
        myList = []
        jsonNameListDicts = self.toJsonNameListDict()
        n=0
        for jsonNameDicts in jsonNameListDicts:
            myDict = jsonNameDicts
            myDict.update(self.toReadJson()[n])
            n += 1
            myList.append(myDict)    
        return myList
    
    
    #以列表字典形式，获得指定目录下，全部目录名、文件名、文件文本数据(读json文件形式)。应用：video.py
    def toVideoListDict(self):
        try:
            myList = []
            iddirs = self.toIdDirListTuple()
            if not isinstance(iddirs,list):
                return 'iddirs err!-----'+iddirs
                
            for iddir in iddirs:               
                myid = iddir[0]
                Dir = iddir[1]#获得不含路径父目录Dir
                dir = myid + '_' + Dir # dir = 0_flask
                 
                dir = self.dirPath + dir  # dir = 'edustack/static/oday/video/0_flask' dir = 'edustack/static/oday/video/1_CCTV' ...               
                publicdict = readJson(dir + '/public.json') #字典
                mp4FileListDicts = MyFile(dir,['.mp4']).toFileNameListDict()                 
                mp4Names = MyFile(dir,['.mp4']).toNameList()
               
                n = 0
                for mp4Name in mp4Names:
                    myDict = {}
                    jsonName = mp4Name.split('.')[0] + '.json'#关联，用MP4文件名做视频简介名 
                    descriptiondict = readJson(jsonName) #字典
                    myDict['myid'] = myid #获得myid
                    myDict['fname'] = os.path.split(mp4Name)[-1][:-4]
                    myDict['coursname'] = Dir #约定：父目录名是总课程名
                    myDict['teacherimg'] =  MyFile(dir,['teacherimg']).toNameList()[0]
                    myDict['courseimg'] =  MyFile(dir,['courseimg']).toNameList()[0]
                    myDict['courseno'] = n + 1                  
                    myDict.update(descriptiondict) #两个字典元素相加
                    myDict.update(publicdict) 
                    myDict.update(mp4FileListDicts[n])
                    n += 1
                    myList.append(myDict)

            return myList
        except Exception as e:
            return  "toVideoListDict() err! " + str(e)
        
    #以列表字典形式，获得指定目录下指定类型的全部文件名、文本。[{'文件名1':'文本1'}...]           
    def toNameTxt(self):
        try:
            filenames = MyFile(self.dirPath,self.strList).toNameList()
            return toFileNameTxt(filenames)
        except Exception as ex:
            return  "toNameTxt() err! "  + str(ex)
    #判断指定目录（指定文件类型）下，是否有文件名    
    def isFileName(self,fname):
        filenames = MyFile(self.dirPath,self.strList).toNameList()
        return any([i == fname for i in filenames])
            
 

#以列表字典形式，获得含路径文件名列表['文件名1','文件名2',...]的全部文件名、文本。[{'.../文件名1':'文本1'}...]  
def toFileNameTxt(filenames):
    FileList = []
    for filename in filenames:
        #filename=filename.decode('UTF-8')#将Python字符串转换成Unicode
        FileDict = {}#字典放在这里是必须的        
        FileDict[filename] = GetTxtfile(filename)#该函数已经将Python字符串转换成Unicode
        FileList.append(FileDict)
    return FileList

#{'a':1},{'b1':11} 获得 {'a': [1,11]}  
def dictValueAdd(myDict1,myDict2):
    myDict1[myDict1.keys()[0]] = [myDict1.values()[0],myDict2.values()[0]]
    return myDict1

#2个列表，键值相加[{'a1':1},{'a2':2}], [{'b1':11},{'b2':12}] 获得 [{'a1': [1,11]},{'a2': [2,12]}] 
def listdictValueAdd(mylistDict1,mylistDict2):
    return  [dictValueAdd(mylistDict1[n],mylistDict2[n]) for n in range(0,len(mylistDict1))] 


#以列表字典形式，获得不含路径文件名列表['文件名1','文件名2',...]的全部文件名、文本。[{'文件名1':'文本1'}...]  
def toFNameTxt(filenames):
    FileList = []
    for filename in filenames:
        FileDict = {}#字典放在这里是必须的 
        FileDict[filename.split('/')[-1]] = GetTxtfile(filename)#该函数已经将Python字符串转换成Unicode
        FileList.append(FileDict)
    return FileList

# 搜索获得指定路径下所有源文件的文件名、文件内容列表字典,同时获得该目录txt目录下所有*.txt的文件名、文件内容列表字典。
# dir指定路径下存放*.py、*.html源文件,filetype文件类型,q搜索。关于功能介绍：目录设定功能介绍dir + txt；  文件名与filetype文件类型文件名相同，扩展名为.txt  2017.5.20
# dir = 'edustack/static/oday/htmlfile/' 文件存放路径；filetype = 'html' 文件类型； q='py'
def searchTxt(dir,filetype,q):
    toNameList = MyFile(dir,[filetype]).toNameList() #获得所有源文件名 列表
    filenames = searchList(toNameList,q) #搜索获得新的源文件名 列表
    myFileNameTxtListDict = toFNameTxt(filenames) #由文件名列表，获得源文件名、文件内容列表字典

    # 功能介绍. 文件目录设定dir + txt；文件名与源文件名相同，扩展名为.txt
    filenames = [os.path.splitext(filename)[0] + ".txt" for filename in filenames]; #设定扩展名为.txt   文件类型列表
    filenames = [os.path.split(filename)[0]+"/txt/"+os.path.split(filename)[1] for filename in filenames]; #设定功能介绍目录txt  
    txtnamesListDict = toFNameTxt(filenames) #由文件名列表，获得功能介绍文件名、文件内容列表字典  
    myFileNameTxtListDict = listdictValueAdd(myFileNameTxtListDict,txtnamesListDict)
    return myFileNameTxtListDict

import json
#读json格式文件，返回字典
def readJson(filepath):
    try:
        with open(filepath) as fp:        
            return json.load(fp)
    except Exception as ex:
        return str(ex)
           
#字典写入json格式文件，json格式文件的文本内容是字典形式    
def writeJson(filepath,myDict): 
    try:
        fp = open(filepath,'w+')
        fp.write(json.dumps(myDict))
        fp.close() 
        return True
    except Exception,ex:
        return False
    
# 当前目录下，创建测试文件       
def createjsonfile(dir):
    dir +='/testMyFile/'
    if not writeJson(dir + "json1.json",{"mystr":"hello","index":"html"}):
        return  "create json1.json err!"
    if not writeJson(dir + "json2.json",{"file":"world"}):
        return  "create json2.json err!"

# 当前目录下，创建测试目录及文件    
def createTestDir(dir,createDir): 
#    dir = os.getcwd()#当前目录,即为myFile.py文件所在的目录 
    if not os.path.isdir(dir + '/testMyFile/' + createDir):
        os.chdir(dir + '/testMyFile/') # 改变目录  .../myAPI/testMyFile
        os.mkdir(createDir) # 创建目录  .../myAPI/testMyFile
        os.chdir(dir + '/testMyFile/' + createDir) # 改变目录  .../myAPI/testMyFile/createDir
        txtFileTest()
        pyFileTest()
        dirTest(dir,createDir)        
        os.chdir(dir) # 改变目录 .../myAPI
        
        
def txtFileTest():
    fp = open("test1.txt",'w')
    fp.write("test1")
    fp.close()
    fp = open("test2.txt",'w')
    fp.write("a\n test2\nb\n")
    fp.close()
    fp = open("test3.txt",'w')
    str = "测试3 test3".encode('UTF-8')#将Unicode转换成Python字符串:"编码(encode)"
    fp.write(str)
    fp.close()
    
def pyFileTest():
    fp = open("test.py",'w')
    fp.write("{'name':'filename'}")
    fp.close() 
       
def dirTest(dir,createDir): 
    if not os.path.isdir(dir + createDir + '/1_testdir1'):    
        os.mkdir('1_testdir1')
    if not os.path.isdir(dir+ createDir + '/2_testdir2'):    
        os.mkdir('2_testdir2')        
    if not os.path.isdir(dir+ createDir + '/.DS_Store'):    
        os.mkdir('.DS_Store')       
    
def delTestDir():
    import shutil
    dir=os.getcwd()# 获得当前目录
    if not os.path.isdir(dir+'/testMyFile'):
        print(dir+'/testMyFile'+"。 del testMyFile err !")
        return False
    print("******",dir)    
    shutil.rmtree("testMyFile") #删除目录，以及目录下所有目录及文件。
    dir=os.getcwd()
    print("=====",dir)
    raise
    return True 

#如果文件名含有中文，获得n个随机字符，做文件名；如果文件名是英文，直接返回英文文件名。
def isChinese(filename,n): # filename='/static/upload/upfile/swfobject.js/'，
    import re
    import string
    import random
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    if zhPattern.search(filename): #判断字符串是否有汉字
        #解决不支持中文问题，获得n个随机字符，做文件名
        fname = string.join(random.sample(
            ['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k',
             'j','i','h','g','f','e','d','c','b','a'], n)).replace(' ','')
        Ext = os.path.splitext(filename)[1]#获得文件扩展名 
        newfname = fname + Ext #获得文件名（扩展名）
        #获得一个路径的目录名eg[0]和文件名eg[1]
        eg = os.path.split(filename)#获得一个路径的目录名
        newfilename = eg[0] + '/'+newfname #获得一个含路径的目录名、文件名
        return newfilename    
    return filename

# 功能：由文件名获得文本文件的行数、文本。优点:排除文本文件最后的不可见字符行，测量准确度高,速度快。
#错误：返回0，‘’。filename支持文件编码格式：GB2312(ANSI) 'utf-8'(UTF-8)
def GetfileLineTxt(filename):
    try:
        n,count,scode =1,0,''
        for line in open(filename, 'r'):
            if line.strip(): #删除两端的不可见字符,判断一行字符是否是可见字符
                count=n
                scode+=line                
            n+=1        
        return count,scode.decode('UTF-8')#将Python字符串转换成Unicode 
    except Exception,ex:
        return 0,''
    
# 功能：由文件名获得文本文件的文本。    
def GetTxtfile(filename):
    try:
        scode = ''
        for line in open(filename, 'r'):
            if line.strip(): #删除两端的不可见字符,判断一行字符是否是可见字符
                scode+=line               
        return scode.decode('UTF-8')#将Python字符串转换成Unicode  
    except Exception,ex:
        return ''

#获得文本文件中的startstr,endstr块文本。注意：startstr,endstr都必须是唯一的行文本，并且startstr行 < endstr行
def GetfileTxt(filename,startstr,endstr):
    try:
        scode = ''
        for line in open(filename, 'r'):
            if line.strip(): #删除两端的不可见字符,判断一行字符是否是可见字
                scode+=line 
        scodelist = scode.split('\n')
        scodelist = scodelist[scodelist.index(startstr) : scodelist.index(endstr) + 1]               
        myscode="\n".join(scodelist)
        return myscode.decode('UTF-8')#将Python字符串转换成Unicode
    except Exception,ex:
        return ''#错误：返回‘’。
#-------------------------------------------------------------------------------------------
# 功能：写文件到硬盘函数。应用场合:上传文件，fread=reg.FILES['upfile']。每次读文件大小size
# 输入：注意：fread=open(readfilepath,'rb') 是文件流，不是文件路径。 输出文件路径writefilepath。
# 输出：返回 成功：return True 失败：return False
#-------------------------------------------------------------------------------------------
def WriteFile(fread,writefilepath):
    size=1024#每次读字节数
    fp = open(writefilepath,'w+') #打开文件
    try:
        while True:
            chunk = fread.read(size)
            if not chunk:
                break
            fp.write(chunk)
            #yield chunk
        fp.close()
    except:
        fp.close()
        return False
    return True

#读一文件写到另外一个文件中 readfilepath、writefilepath两个都是带路径的文件名   2017.6.6
def ReadWriteFile(readfilepath,writefilepath):
    fread = open(readfilepath,'rb') #打开文件 
    return True if WriteFile(fread,writefilepath) else False

# 当前目录:即为本文件myFile.py所在的目录 .../edustack/myAPI
class testUnitMyFile(unittest.TestCase):
    dir = os.getcwd()
    #print(dir);# /Users/wuchunlong/local/Project-Account-Online-master/mysite/account/myAPI
    if 'myAPI' in dir:
        createjsonfile(dir)
        createTestDir(dir,'testMyFile')
        createTestDir(dir,'testMyFile1')

    def test_toNameList_txt(self):
        dir = os.getcwd() + '/testMyFile'
        myfile = MyFile(dir + '/testMyFile',['.txt'])  # dir + '/testMyFile' 为绝对目录
        self.assertEquals(myfile.toNameList(),[dir + '/testMyFile/test1.txt', 
                                               dir + '/testMyFile/test2.txt',
                                               dir + '/testMyFile/test3.txt'])                                           
              
    def test_toNameList_py(self):
        myfile = MyFile('testMyFile/testMyFile',['.py'])  # 'testMyFile' 为当前目录下的相对目录
        self.assertEquals(myfile.toNameList(),['testMyFile/testMyFile/test.py'])
  
     
    def test_toNameList_txt_py(self):
        myfile = MyFile('testMyFile/testMyFile',['.txt','.py'])
        self.assertEquals(myfile.toNameList(),['testMyFile/testMyFile/test.py', 
                                                'testMyFile/testMyFile/test1.txt',
                                                'testMyFile/testMyFile/test2.txt',
                                                'testMyFile/testMyFile/test3.txt'])
  
    def test_toNameList(self):
        myfile = MyFile('testMyFile/testMyFile',[])
        self.assertEquals(myfile.toNameList(),['testMyFile/testMyFile/1_testdir1',
             'testMyFile/testMyFile/2_testdir2', 'testMyFile/testMyFile/test.py', 
             'testMyFile/testMyFile/test1.txt', 'testMyFile/testMyFile/test2.txt',
             'testMyFile/testMyFile/test3.txt'])    
    def test_toDirList(self):
        myfile = MyFile('testMyFile/testMyFile',[])
        self.assertEquals(myfile.toDirList(),['testMyFile/testMyFile/1_testdir1',
                                              'testMyFile/testMyFile/2_testdir2'])
                                              
  
    def test_toFileNameListDict_txt(self):
        myfile = MyFile('testMyFile/testMyFile',['.txt'])
        self.assertEquals(myfile.toFileNameListDict(),
                                                [{'filename':'/testMyFile/test1.txt'},
                                                 {'filename':'/testMyFile/test2.txt'},
                                                 {'filename':'/testMyFile/test3.txt'}])
           
              
    def test_toIdDirListTuple(self):
        myfile = MyFile('testMyFile/testMyFile',[])
        self.assertEquals(myfile.toIdDirListTuple(),[('1', 'testdir1'), ('2', 'testdir2')])
                                                
    def test_toNameTxt(self):
        myfile=MyFile('testMyFile/testMyFile',['.txt'])
        self.assertEquals(myfile.toNameTxt(),[{'testMyFile/testMyFile/test1.txt': 'test1'},
                                               {'testMyFile/testMyFile/test2.txt': u'a\n test2\nb\n'}, 
                                               {'testMyFile/testMyFile/test3.txt': '\u6d4b\u8bd53 test3'}])
                                                 
    def test_dictValueAdd(self):
        self.assertEquals(dictValueAdd({'a':'b'},{'a1':'c'}),{'a': ['b','c']}) 
          
    def test_listdictValueAdd(self):        
        self.assertEquals(listdictValueAdd([{'a1':1},{'a2':2}], [{'b1':11},{'b2':12}]),
                          [{'a1': [1,11]},{'a2': [2,12]}])         
      
      
      
    def test_WriteJson(self):      
        myDict={'test' :'ok'}
        #myDict=[1,2]
        filepath = 'testMyFile/testJson.json' 
        self.assertEquals(writeJson(filepath,myDict),True) 
     
    def test_WriteFile(self):
        filename  = os.getcwd() + '/testMyFile/json1.json'
        fread = open(filename,'rb') #打开文件
        writefilepath  = os.getcwd() + '/testMyFile/testMyFile/1_testdir1/json1.json'
        self.assertEquals(WriteFile(fread,writefilepath),True)
  
    def test_ReadWriteFile(self):
        filename  = os.getcwd() + '/testMyFile/json1.json'
        writefilepath  = os.getcwd() + '/testMyFile/testMyFile/1_testdir1/WriteFilejson1.json'
        self.assertEquals(ReadWriteFile(filename,writefilepath),True)
      
    def test_ReadJson(self):            
        filepath = 'testMyFile/testJson.json' 
        self.assertEquals(readJson(filepath),{'test' : 'ok'}) 
  
    def test_ReadJson_type(self):            
        filepath = 'testMyFile/testJson.json' 
        self.assertEquals(type(readJson(filepath)),dict)
            
           
    def test_toReadJson(self):
        dir = os.getcwd()  + '/testMyFile'       
        myfile = MyFile(dir,['.json']) 
        self.assertEquals(myfile.toReadJson(),[{u'index': u'html', u'mystr': u'hello'},
                                               {u'file': u'world'},{u'test': u'ok'}])
          
    def test_toJsonNameListDict(self):
        dir = os.getcwd()  + '/testMyFile'            
        myfile = MyFile(dir,['.json']) 
        self.assertEquals(myfile.toJsonNameListDict(),
                    [{'name': u'json1'}, {'name': u'json2'}, {'name': u'testJson'}])
  
    def test_toJsonListDict(self):
        dir = os.getcwd()    + '/testMyFile'            
        myfile = MyFile(dir,['.json']) 
        self.assertEquals(myfile.toJsonListDict(),
            [{u'index': u'html', u'mystr': u'hello', 'name': u'json1'},
            {u'file': u'world', 'name': u'json2'},{'name': u'testJson', u'test': u'ok'}])
            
    def test_isChinese(self):            
        filename = '/static/upload/upfile/swfobject.mp4' #任何字符串都可以
        self.assertEquals(isChinese(filename,6),
            '/static/upload/upfile/swfobject.mp4')
          
    def test_isChinese_Ch(self):            
        filename = u'/static/upload/upfile/CH1234中国.mp4'#任何字符串都可以
        ischinese = isChinese(filename,6)
        self.assertEquals(ischinese,ischinese)
  
    def test_toDirDownFileNameList_py(self):
        dir = os.getcwd() + '/testMyFile'
        myfile = MyFile(dir,[])
        #列表形式，获得指定.../edustack/upvideo目录下 所有二级目录：testMyFile、testMyFile1
        #全部含路径的*.py文件
        self.assertEquals(myfile.toDirDownFileNameList(".py"),
            [dir + '/testMyFile/test.py',dir + '/testMyFile1/test.py'])
  
  
    def test_toDirDownFileNameFNameListDict_py(self):
        dir = os.getcwd() + '/testMyFile'
        myfile = MyFile(dir,[])
        #列表形式字典，获得指定.../edustack/upvideo目录下 所有二级目录：testMyFile、testMyFile1
        #全部含路径的*.py文件和不含路径的*.py
        self.assertEquals(myfile.toDirDownFileNameFNameListDict(".py"),
            [{'fname': u'test.py', 'filename': dir + '/testMyFile/test.py'},
             {'fname': u'test.py', 'filename': dir + '/testMyFile1/test.py'}])
          
    def test_toDirDownFileNameFNameListDict_txt(self):
        dir = os.getcwd() + '/testMyFile'
        myfile = MyFile(dir,[])
        #列表形式字典，获得指定.../edustack/upvideo目录下 所有二级目录：testMyFile、testMyFile1
        #全部含路径的*.txt文件和不含路径的*.txt        
        self.assertEquals(myfile.toDirDownFileNameFNameListDict(".txt"),
            [{'fname': u'test1.txt', 'filename': dir + '/testMyFile/test1.txt'},
             {'fname': u'test2.txt', 'filename': dir + '/testMyFile/test2.txt'}, 
             {'fname': u'test3.txt', 'filename': dir + '/testMyFile/test3.txt'},
             {'fname': u'test1.txt', 'filename': dir + '/testMyFile1/test1.txt'},
             {'fname': u'test2.txt', 'filename': dir + '/testMyFile1/test2.txt'}, 
             {'fname': u'test3.txt', 'filename': dir + '/testMyFile1/test3.txt'}])
  
  
    def test_GetfileLineTxt(self):
        filename  = os.getcwd() + '/testMyFile/json1.json'
        self.assertEquals(GetfileLineTxt(filename),(1, '{"index": "html", "mystr": "hello"}'))
    def test_GetfileLineTxt_err(self):
        filename  = os.getcwd() + "/testMyFile/testMyFile/test3.txt"
        self.assertEquals(GetfileLineTxt(filename),(1, u'\u6d4b\u8bd53 test3'))#测试中文 文本文件

    def test_GetTxtfile(self):
        filename  = os.getcwd() + "/testMyFile/testMyFile/test3.txt" 
        self.assertEquals(GetTxtfile(filename),'\u6d4b\u8bd53 test3')#测试中文 文本文件
        
    def test_GetfileTxt(self):
        filename  = os.getcwd() + "/testMyFile/testMyFile/test2.txt"
        self.assertEquals(GetfileTxt(filename,'a','b'),u'a\n test2\nb') 
    
    def test_isFileName1(self):
        dir = os.getcwd() + '/testMyFile'
        self.assertEquals(MyFile(dir,['json']).isFileName(dir+'/json1.json'),True)        
    def test_isFileName2(self):
        dir = os.getcwd() + '/testMyFile'
        self.assertEquals(MyFile(dir,['json']).isFileName(dir+'/json3.json'),False)        
#     def test_GetEncoding(self):
#         self.assertEquals(GetEncoding('hello'),'')         
#-------------------------------------------------------------------------------------------
# 引用：import chardet
# 函数: def GetEncoding(strcode):
# 功能：获得字符串strcode编码格式
# 输入：strcode字符串
# 输出：返回 可信度、编码 字典
# 版本：ver2.1
# 作者：吴春龙    时间：2016.7.17
# 测试环境：python2.7
#    getEncoding=GetEncoding('hello')
#    结果：
#    getEncoding={'confidence': 0.99, 'encoding': 'GB2312'}
#-------------------------------------------------------------------------------------------
#import chardet
# def GetEncoding(strcode):
#     getEncoding=chardet.detect(strcode)
#     return getEncoding#['encoding']  #还是应该获得可信度的

   

    #delTestDirFile()         
if __name__ == '__main__':
    unittest.main()
    
    
'''   
#-------------------------------------------------------------------------------------------
# 函数: GetFileEncoding(filename):
# 功能：获得filename文件编码格式 空返回 'None'
# 输入：filename文件名字符串
# 输出：返回  可信度、编码 字典
# 应用背景，如果要对一个大文件进行编码识别，使用这种高级的方法，可以只读一部，去判别编码方式从而提高检测速度。
# 版本：ver2.1
# 作者：吴春龙    时间：2016.7.17
# 测试环境：python2.7
#    filename文件名字符串类型，获得文件编码格式
#    filename=u'static/oday/Html__File/计算阶乘gb2312.html'
#    getEncoding=GetFileEncoding(filename)
#    结果：
#    getEncoding={'confidence': 0.99, 'encoding': 'GB2312'}
#-------------------------------------------------------------------------------------------
def GetFileEncoding(filename):
    from chardet.universaldetector import UniversalDetector
    detector = UniversalDetector() #创建一个检测对象
    for line in open(filename,'r'):
        detector.feed(line)#分块进行测试，直到达到阈值
        if detector.done:
            break
    detector.close()#关闭检测对象
    return detector.result #输出检测结果

#-------------------------------------------------------------------------------------------
# 函数: def IsCodeUTF8(strcode):
# 功能：判断字符串是否是UTF-8编码
# 输入：strcode字符串
# 输出：返回 True False
# 版本：ver2.1
# 作者：吴春龙    时间：2016.7.17
# 测试环境：python2.7
def IsCodeUTF8(strcode):
    getEncoding=GetEncoding(strcode)
    getEncoding=getEncoding['encoding']
    if (getEncoding[:5]=='UTF-8')|(getEncoding[:5]=='utf-8'):
        return True
    return False

#-------------------------------------------------------------------------------------------
# 函数: def IsFileUTF8(filename):
# 功能：判断文件是否是UTF-8编码
# 输入：filename文件名字符串
# 输出：返回 True False
# 版本：ver2.1
# 作者：吴春龙    时间：2016.7.17
# 测试环境：python2.7
#    filename=u'static/oday/Html__File/计算阶乘gb2312.html'
#    if IsFileUTF8(filename):
#        return HttpResponse('y')
#    return HttpResponse('n')
#-------------------------------------------------------------------------------------------
def IsFileUTF8(filename):
    getFileEncoding=GetFileEncoding(filename)
    if (getFileEncoding['encoding'][:5]=='UTF-8')|(getFileEncoding['encoding'][:5]=='utf-8'):
        return True
    return False

#-------------------------------------------------------------------------------------------
# 函数: def TexFileToUTF_8(filename):
# 功能：将filename文本文件编码格式：统一转换为 UTF-8编码文件。支持所有编码。常用：GB2312(ANSI) 'utf-8'(UTF-8) UTF-16LE(Unicode),
# 输入：filename文件名字符串
# 输出：返回 True False
# 版本：ver3.1
# 作者：吴春龙    时间：2016.7.18
# 测试环境：python2.7
#-------------------------------------------------------------------------------------------
def TexFileToUTF_8(filename):
    fp = open(filename,'r') #打开文本文件
    htmlcode=fp.read()

    if IsCodeUTF8(htmlcode): #判断是否UTF-8编码
        fp.close()
        return True

    #处理 转换为UTF_8编码
    try:
        fp = open(filename,'w')
        getEncoding=GetEncoding(htmlcode)#获得字符串htmlcode编码格式 。  常用html文件编码格式：GB2312(ANSI)、'UTF-8-SIG'(UTF-8)、 'utf-8'(UTF-8)
        getEncoding=getEncoding['encoding']
        htmlcode=htmlcode.decode(getEncoding).encode('utf-8')# 转换为'utf-8'。支持所有编码

    except Exception,ex:
        print('TexFileToUTF_8 err:',ex)
        fp.close()
        return False
    fp.write(htmlcode)
    fp.close()
    return True

#-------------------------------------------------------------------------------------------
# 函数: def TexFileAllToUTF_8(FindPath,FlagStr):
# 功能：将指定目录下指定类型的所有文件编码,统一转换成UTF-8编码。如果原来就是UTF-8，直接通过。支持所有编码。
# 输入：FindPath指定目录，FlagStr=['html']指定文件类型
# 输出：返回 True False
# 版本：ver3.1
# 作者：吴春龙    时间：2016.7.18
# 测试环境：python2.7
#    FindPath='static/oday/Html__File'  将该目录下，所有html文件,统一转换成UTF-8编码。如果原来就是UTF-8，直接通过。
#    if TexFileAllToUTF_8(FindPath,FlagStr=['html']):
#        return HttpResponse('y')
#    return HttpResponse('n')
#-------------------------------------------------------------------------------------------
def TexFileAllToUTF_8(FindPath,FlagStr):
    try:
        FileList=GetFileList(FindPath,FlagStr)
        for filename in FileList:
            TexFileToUTF_8(filename)
        return True
    except Exception,ex:
        print('TexFileAllToUTF_8 err:',ex)
        return False



#-------------------------------------------------------------------------------------------
# 函数: def GetfileLineTxt(filename):
# 功能：由文件名获得文本文件行数。最大优点:测量准确度高.排除文本文件最后的不可见字符行。支持filename文件编码格式：GB2312(ANSI) 'utf-8'(UTF-8)
# 输入：filename文件名字符串
# 输出：返回 行数整数
# 版本：ver2.1
# 作者：吴春龙    时间：2016.7.11
# 测试环境：python2.7
#-------------------------------------------------------------------------------------------
def GetfileLineNum(filename):
    count,n=0,1
    for line in open(filename, 'r'):
        if line.strip(): #删除两端的不可见字符,判断一行字符是否是可见字符
            count=n
        n+=1
    return count

#-------------------------------------------------------------------------------------------
# 函数: def GetfileLineTxt(filename):
# 功能：读文件，按列表方法使用
# 测试环境：python2.7
#    yield生成器读文件，不会造成内存过大开销。使用方法如下：
#    strcodes=ReadFileYield(filename )#yield生成器读文件，不会造成内存过大开销
#    for strcode in strcodes:
#        if strcode!='':
#            return strcode
#-------------------------------------------------------------------------------------------
def ReadFileYield(filename ):
    chunk_size=1024 #每次读字节数
    f = open(filename, "rb")  # 二进制文件中的所有数据
    while True:
        c = f.read(chunk_size)
        if c:
            yield c
        else:
            break
    f.close()

#-------------------------------------------------------------------------------------------
# 函数: def JiebaSearchFileTxt(request,searchstr,filedirpath,FlagStr):
# 功能：分词  搜索指定目录下的文件名函数。返回文件名列表。
# 输入：searchstr搜索字符串,filedirpath文件存放目录,FlagStr=['F','EMS','txt'] 要求文件名称中包含这些字符
# 输出：返回 文件名列表
# 版本：ver2.1
# 作者：吴春龙    时间：2016.7.3
# 测试环境：python2.7
#    searchstr='字符串'#搜索字符串
#    filedirpath=u'static/oday/PythonFile/'#Python文件存放目录
#    searchList=JiebaSearchFile(request,searchstr,filedirpath,FlagStr=['html']) #调用分词搜索指定目录下的文件名函数
#    return HttpResponse(searchList)
#-------------------------------------------------------------------------------------------
def JiebaSearchFileTxt(request,searchstr,filedirpath,FlagStr):
    try:
        FileList1=[] #文件名列表
        MyJiebaList= list(jieba.cut(searchstr, cut_all = True)) # 获得中文分词列表
        getFileLists=GetFileTxtList(filedirpath,FlagStr)#获得目录下文件名列表
        for getFileList in getFileLists:
            if IsListSubStr(MyJiebaList,getFileList['filename']):#判断分词列表是否在filename字符串中
                FileList1.append(getFileList) #添加到数组
        FileList1=ListDictDelRepeat(FileList1,'filename')#列表含字典去重
        return FileList1
    except Exception,ex:
        print('JiebaSearchFileTxt err:',ex)
        return ''

def JiebaSearchFileTxt123(request,searchstr,filedirpath,FlagStr):
    try:
        FileList=[] #文件名列表
        MyJiebaList= list(jieba.cut(searchstr, cut_all = True)) # 获得中文分词列表
        getFileLists=GetFileList(filedirpath,FlagStr)#获得目录下文件名列表
        for getFileList in getFileLists:
            if IsListSubStr(MyJiebaList,getFileList):#判断分词列表是否在filename字符串中
                FileList.append(getFileList) #添加到数组
                #FileList=list(set(FileList))#列表去重?
        return FileList
    except Exception,ex:
        print('JiebaSearchFile err:'*9,ex)
        return ''

'''
    

