CSRF_ENABLED = True
SECRET_KEY = 'com.buaa.exit'

import os
basedir = os.path.abspath(os.path.dirname(__file__))
 
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WHOOSH_BASE = os.path.join(basedir, 'search.db')

BOOK_PER_PAGE = 8
ITEM_PER_PAGE = 6
UPLOAD_FOLDER = 'app/static/upload'
img_ext = ['.gif','.jpg','.jpeg','.png','.bmp']