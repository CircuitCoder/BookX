from app.models import User
from app import db
import hashlib

user = User(username = 'admin',
            password = hashlib.new('md5','admin').hexdigest(),
            mail = 'admin@admin.com',
            tel = '18812345678',
            school = 'BUAA',
            address = 'BUAA',
            is_admin = True,
            is_ban = False)

db.session.add(user)
db.session.commit()