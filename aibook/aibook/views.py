from django.shortcuts import render, redirect
from . import aibook_db as db

# 登录
def login(request):
    if request.method == 'GET':  # 如果直接输URL，进入登录页面
        return render(request, 'login.html')
    if request.method == 'POST':  # 如果提交了表单
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        arr=db.query_user_byuname(uname)
        if arr:  # 数据库有这个用户
            if pwd==arr[0]['pwd']:  # 如果密码正确,应跳转到主页
                request.session['uname']=uname
                request.session['uid'] = arr[0]['uid']
                return redirect('/index/')
            else:
                return render(request, "login.html", {'error': '用户名或密码错误'})
        else:  # 数据库没有，则注册用户
            db.insert_user(uname,pwd)
            arr = db.query_user_byuname(uname)
            request.session['uname'] = uname
            request.session['uid'] = arr[0]['uid']
            return redirect('/index/')

def index(request):
    if request.session.get('uname'):  # 只有登录才能进入主页
        context = {}
        context['uname'] = request.session.get('uname')
        if request.method == 'POST':  # 如果是查询
            bname = request.POST.get('bname')
            books=db.search_books(bname)
        else:
            books = db.query_all_books()  # 获取所有图书列表
        context['book_num']=len(books)
        context['books'] = books
        return render(request, "index.html", context)
    else:  # 未登录则跳转登录页面
        return render(request, 'login.html')

def logout(request):  # 退出登录
    if request.session.get('uname') != None:
        del request.session["uname"]
    return render(request, 'login.html')

def book(request): # 进入图书信息界面
    if request.session.get('uname') != None:
        context={}
        bid = request.GET.get('bid')
        book=db.get_book_bybid(bid)
        # 获得简介
        intro = book['intro'].split('<br>')
        # 获得标签
        tags = book['tags'].split('/')
        # 获得所有评论
        comments = db.query_comments_bybid(bid)
        context['book'] = book
        context['uname'] = request.session.get('uname')
        context['intro'] = intro
        context['tags'] = tags
        context['comments']=comments
        context['comment_num']=len(comments)  # 判断是否有评论
        return render(request,'book.html',context)
    else:
        return render(request, 'login.html')

def comment(request): # 增加评论
    uid=request.session.get('uid')
    bid=request.POST.get('bid')
    ccontent=request.POST.get('ccontent')
    db.add_comments(uid,bid,ccontent)
    return redirect('/book?bid={}'.format(bid))

def recommend(request): # 图书推荐
    books = db.get_recommend_books()
    context = {}
    if not request.GET.get('tag'):  # 如果没有标签参数
        context['books'] = books
        context['book_num'] = len(books)
    else:  # 如果有标签参数
        tag = request.GET.get('tag')
        if tag and tag != '':  # 如果有输入标签
            ls = []
            for book in books:
                tags = book['tags'].split('/')
                if tag in tags:
                    ls.append(book)  # 加入推荐列表
            context['books'] = ls
            context['book_num'] = len(ls)
        elif tag == '':
            context['books'] = books
            context['book_num'] = len(books)
    return render(request, 'recommend.html',context)

def add_tag(request):
    ntag=request.POST.get('ntag')
    bid=request.POST.get('bid')
    book=db.get_book_bybid(bid)
    tags=book['tags'].split('/')
    if ntag not in tags:  # 如果是新标签，则更新tags
        tags.append(ntag)
        ntags='/'.join(tags)
        db.add_tag(bid,ntags)
    return redirect('/book?bid={}'.format(bid))




