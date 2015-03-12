#-*- coding:utf-8 -*- 

from flask import request,render_template, g, flash, url_for, redirect, abort
from flask.ext.login import login_required
from app import app, db
from models import User, Book,Give,Get
from datetime import datetime
from config import ITEM_PER_PAGE

@app.route('/user')
@app.route('/user/infomation')
@login_required
def user():
    user = User.query.get(g.user.id)
    if not user:
        abort(404)
    
    if user.is_admin:
        return redirect(url_for('administrator'))
        
    return render_template('user.html',
                            g = g,
                            user = user)

@app.route('/user/u_give')
@app.route('/user/u_give/<int:page>')
@login_required
def u_give(page=1):
    user = User.query.get(g.user.id)
    if not user:
        abort(404)

    gives = user.gives.order_by(Give.time.desc()).paginate(page,ITEM_PER_PAGE,True)
    return render_template('u_give.html',
                            g = g,
                            user = user,
                            gives = gives)

@app.route('/user/u_get')
@app.route('/user/u_get/<int:page>')
@login_required
def u_get(page=1):
    user = User.query.get(g.user.id)
    if not user:
        abort(404)

    gets = user.gets.order_by(Get.time.desc()).paginate(page,ITEM_PER_PAGE,True)
    return render_template('u_get.html',
                            g = g,
                            user = user,
                            gets = gets)

@app.route('/give/<int:b_id>')
@login_required
def give(b_id):
    give = Give(author = g.user.id,
                book_id =b_id,
                time = datetime.now(),
                status = 0)  
    db.session.add(give)
    db.session.commit()
    flash("添加成功，等待管理员审核")
    return redirect(url_for('info',b_id=b_id))



@app.route('/get/<int:b_id>')
@login_required
def get(b_id):
    b = Book.query.get(b_id)
    if not b:
        flash("没有这本书",'error')
    elif b.num == 0:
        flash("剩余零本",'error')
    else:
        b.num = b.num - 1
        db.session.add(b)
        db.session.commit()
        get = Get(author = g.user.id,
                    book_id =b_id,
                    time = datetime.now(),
                    status = 0)  
        db.session.add(get)
        db.session.commit()
        flash("预订成功，等待管理员审核")
    return redirect(url_for('info',b_id=b_id))
