#-*-coding:utf-8-*- 支持中文
'''
测试在'edustack/views/test.py'
2016.11.04
'''
from django.http.response import HttpResponseRedirect, HttpResponse,\
    StreamingHttpResponse
from myFile import isChinese #工程中使用的类

#下载文件  函数    2016.11.04
# 1、下载资源时，不支持中文文件名。解决方法：若下载资源是中文文件名，则随机产生n个字符（a-x）做为文件名。
# 2、支持所有文件下载。包括图像文件。
# 3、#应用测试在： tests.py
def downLoadFile(filename):
    downfilename = isChinese(filename,4).split('/')[-1]
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(downfilename)
    return response