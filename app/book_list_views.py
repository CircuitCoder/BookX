#-*- coding:utf-8 -*- 

from flask import request,render_template,g, flash, url_for, redirect
from flask.ext.login import current_user,login_required
from app import app,db
from models import Book,User
from forms import BookForm
from config import BOOK_PER_PAGE
from administrator_views import is_not_admin

def getctgy(search_category):
    category = {u'文学':'literature',
                u'数学':'mathematics',
                u'物理':'physics',
                u'化学':'chemitsry',
                u'出国':'abroad',
                u'其它':'others',
                u'全部分类':'all'}
    if search_category:
        return category[search_category]
    return None


@app.route('/booklist',methods = ['GET','POST'])
@app.route('/booklist/<int:page>',methods = ['GET','POST'])
def booklist(page=1):
    search_category = request.args.get('category')
    bookname = request.args.get('bookname')
    if not search_category:
        search_category=u'全部分类'
    category = getctgy(search_category)
    books = Book.query
    if is_not_admin():
        books = books.filter_by(status = True)
    if not search_category == '全部分类':
        books = books.filter_by(category = search_category)
    if bookname:
        books = books.filter_by(name = bookname)
    books = books.paginate(page,BOOK_PER_PAGE,True)
    return render_template('booklist.html',
                            g = g, 
                            books = books,
                            category = category)