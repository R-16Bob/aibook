# 数据库aibook操作
from aibook_Model.models import Users,Books,Comments

def insert_user(uname,pwd):  # 增加用户
    user = Users()
    user.uname=uname
    user.pwd=pwd
    user.save()

def query_user_byuname(uname):  # 条件查询用户
    result=Users.objects.filter(uname=uname)  # filter相当于where
    arr=[]
    for i in result:
        arr.append({'uid':i.uid,'uname':i.uname,'pwd':i.pwd})
    return arr

def query_all_books():  # 获得所有图书->index
    result=Books.objects.all()
    arr = []
    for i in result:
        content = {'bid':i.bid,'bname':i.bname,'writer':i.writer,'time':i.time,
                   'publisher':i.publisher,'rate':i.rate,'rate_nums':i.rate_nums}
        arr.append(content)
    return arr

def search_books(bname):  # 搜索图书->index
    result = Books.objects.filter(bname__contains=bname)  # 模糊查询
    arr=[]
    for i in result:
        content = {'bid':i.bid,'bname':i.bname,'writer':i.writer,'time':i.time,
                   'publisher':i.publisher,'rate':i.rate,'rate_nums':i.rate_nums}
        arr.append(content)
    return arr

def get_recommend_books():  # 获取按评分和评分人数排序的图书列表
    result = Books.objects.all().order_by('-rate','-rate_nums')
    arr = []
    for i in result:
        content = {'bid': i.bid, 'bname': i.bname, 'writer': i.writer, 'time': i.time,
                   'publisher': i.publisher, 'rate': i.rate, 'rate_nums': i.rate_nums,'tags':i.tags}
        arr.append(content)
    return arr

def get_book_bybid(bid): # 根据bid获取图书所有信息->book
    result = Books.objects.filter(bid=bid)
    i=result[0]
    content = {'bid': i.bid, 'bname': i.bname, 'writer': i.writer, 'time': i.time,
               'publisher': i.publisher, 'rate': i.rate, 'rate_nums': i.rate_nums,
               'price':i.price,'intro':i.intro,'tags':i.tags}
    return content

def add_comments(uid,bid,ccontent):  # 增加评论
    comment = Comments()
    # 对于设置了外键的列需要传对象
    user=Users.objects.filter(uid=uid).first()
    comment.uid=user
    comment.bid=Books.objects.filter(bid=bid).first()
    comment.uname=user.uname
    comment.ccontent=ccontent
    comment.save()

def query_comments_bybid(bid): # 获取一本书的所有评论
    result = Comments.objects.filter(bid=bid)
    arr=[]
    for i in result:
        content = {'uname':i.uname,'ccontent':i.ccontent,
                   'created':i.created}
        arr.append(content)
    return arr

def add_tag(bid,ntags):  # 修改book的标签
    book = Books.objects.get(bid=bid)
    book.tags=ntags
    book.save()
