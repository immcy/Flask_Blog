
from ext import db


class Role(db.Model):
    __tablename__ = "roles"  # db中表明，如果不设置，则会与class同的默认名
    id = db.Column(db.Integer, primary_key=True)  # SQLAlchemy要求必须有主键，一般命名为id即可
    name = db.Column(db.String(50), unique=True)  # 表示name为字符串，不重复
    users = db.relationship("User", backref='role')  # 关联user模型，并在user中添加反向引用(backref)

    # 关于反向引用  本来想直接在查到的Role里直接用Role.users 于是添加了relationship,
    # 想要通过user直user.role呢 还要再写一次。。有了backref就省了一层
    # 不过由于是一对多的关系，user里的foreign key还是要写的 虽然有外键插入会由于要查找是否存在而变慢，但role表小啊 哈哈


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)  # 此列带索引
    password = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))  # 外键指向roles表中的id列

## 不完善版本 还要先在python里 import db 然后db.create_all()
## 然后在外面 python app.py db migrate -m “xx” 等模型改变时还要 python app.py db upgrade
## 先这样吧



