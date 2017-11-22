#-*-coding:utf-8-*- 支持中文
# 单元(类、函数)测试方法：Eclipse环境 选择运行图标 --> Run As --> Python Run 
# pageAPI.py  分页类
# wcl6005@126.com    2017.2.5

class Page(object):
    '''
    用object好处：输入参数的个数可变，可以是1-4个
    Page object for display pages.  2016.9.18
    >>> p1 = Page(100,23,5,4)
    >>> p1.page_count
    20
    >>> p1 = Page(100,23,3,3)
    >>> p1.page_count
    34
    >>> p1 = Page(99,23,3,3)
    >>> p1.page_count
    33
    >>> p1 = Page(100, 19)
    >>> p1.page_bit
    1
    >>> p1 = Page(100, 20)
    >>> p1.page_bit
    2
    >>> p1 = Page(100, 21)
    >>> p1.page_bit
    3
    >>> p1 = Page(100, 22, 4, 3)
    >>> p1.page_bit
    1
    >>> p1 = Page(100, 21, 4, 3)
    >>> p1.page_bit
    3
    >>> p1 = Page(100, 20, 4, 3)
    >>> p1.page_ctrl
    4
    >>> p1 = Page(100, 21, 4, 3)
    >>> p1.page_ctrl
    4
    >>> p1 = Page(100, 22, 4, 3)
    >>> p1.page_ctrl
    4
    >>> p1 = Page(100, 23, 4, 3)
    >>> p1.page_ctrl
    5
    >>> p1 = Page(100, 24, 4, 3)
    >>> p1.page_ctrl
    5
    >>> p1 = Page(100, 25, 4, 3)
    >>> p1.page_ctrl
    5
    
    >>> p1 = Page(100, 23, 4, 3)
    >>> p1.page_bit
    1
    >>> p1 = Page(100, 24, 4, 3)
    >>> p1.page_bit
    2
    >>> p1 = Page(100, 25, 4, 3)
    >>> p1.page_bit
    3
    
    >>> p1 = Page(100, 25, 4, 3)
    >>> p1.toDict()
    {'has_next': False, 'page_index': 25, 'page_count': 25, 'has_previous': True, 'item_count': 100}
    >>> p1 = Page(100, 25, 4, 3)
    >>> p1
    item_count: 100, page_count: 25, page_index: 25, page_size: 4, offset: 96, limit: 4
    '''
    # 项目总数item_count   page_index页索引   page_size每页显示数  pagenav分页按钮数
    def __init__(self, item_count, page_index=1, page_size=4, pagenav=3):

        self.item_count = item_count
        self.page_size = page_size
        self.page_index = page_index  #页索引
        self.page_count = item_count / page_size + (1 if item_count % page_size > 0 else 0)
        if (item_count == 0) or (self.page_count < 1)  or (page_index < 1) or (page_index > self.page_count):
            self.page_index = page_index
            self.page_size = page_size
            self.page_count = item_count / page_size + (1 if item_count % page_size > 0 else 0)
        
        self.offset = self.page_size * (page_index - 1) #偏移，即页开始位置
        self.limit = self.page_size #每页显示数

        if self.page_count <= 3:#总页数 <= 3
            self.page_bit = self.page_index
            self.page_ctrl = self.page_count
        else:#总页数>3   例如：page_count=19
 
            #总页数  page_count>3，处理最后3页前面页的。例如：pageMAX=19  [1--16]
            if self.page_index<(self.page_count-2): #   pageMAX>3    1=< pageInt <17
                self.page_ctrl = 4
                #获得位数page_bit
                self.page_bit=pagenav if (self.page_index % pagenav)==0 else self.page_index%pagenav
 
            #总页数  pageMAX>3， 处理最后3页。 例如：pageMAX=19  [17--19]
            else:      # 17%3=2            正常计算：pageInt=17  pagebit='2'
                self.page_ctrl = 5
                if self.page_index == (self.page_count-2):self.page_bit = 1 
                if self.page_index == (self.page_count-1): self.page_bit = 2
                if self.page_index == self.page_count: self.page_bit = 3


        self.has_next = self.page_index < self.page_count # True False
        self.has_previous = self.page_index > 1 # True False

    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s' % (self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__ = __str__

    def toDict(self):
        return {
            'page_index': self.page_index,
            'page_count': self.page_count,
            'item_count': self.item_count,
            'has_next': self.has_next,
            'has_previous': self.has_previous
    
        }
        
# model支持数据库对象、列表字典对象
def _get_model_by_page(request,model, listRow):#add
    try:
        if not isinstance(model,list):
            model = model.objects.all()
        page=Page(len(model),_get_page_index(request),_get_listRows(request,listRow), 3)#3个按钮
        model=model[page.offset : page.offset + page.limit]
        return model,page
    except:
        return [],1

def _get_page_index(request):
    pageIndex = int(request.GET.get('page', '1'))
    try:
        pageIndex = pageIndex if pageIndex >0 else 1
    except:
        pageIndex = 1
    return pageIndex

def _get_listRows(request,listRow):
    listRows = int(request.GET.get('listRows', listRow))
    try:
        listRows = listRows if listRows>0 else 4
    except:
        listRows = 4
    return listRows        
        
# def get_items_by_page(pageIndex, Model):#保留文相工程
#     total = Model.query.count()
#     page = Page(total, pageIndex)
#     models = Model.query.offset(page.offset).limit(page.limit)
#     return models, page
#  
# def get_items_page(pageIndex, Model, page_size):#保留文相工程 
#     total = Model.query.count()
#     page = Page(total, pageIndex, page_size)
#     models = Model.query.offset(page.offset).limit(page.limit)
#     return models, page 
       
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
    
'''
单元测试结果：
...    
38 tests in 10 items.
38 passed and 0 failed.
Test passed.
'''