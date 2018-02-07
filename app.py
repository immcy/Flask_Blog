from flask import Flask, render_template, \
    redirect, request, abort, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import uuid
from ext import db
from flask_script import Manager
import pymysql
pymysql.install_as_MySQLdb()  # 囧
from flask_migrate import Migrate, MigrateCommand
from models import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:5@localhost/web'
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

bootstrap = Bootstrap(app)
db.init_app(app)     # 推荐用法是这样初始化哦 把导入的包放到ext中 还解决了循环依赖问题
manager = Manager(app)
migrate = Migrate(app, db)  # 配置迁移


manager.add_command("db", MigrateCommand)  # 配置迁移命令


@app.route('/')
def index():
    name = session.get('username')
    print(name)
    if not name:
        return redirect('/login')
    else:
        return render_template('index.html', name=name)


class LoginForm(FlaskForm):
    username = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("登录")


@app.route('/login', methods=["GET", "POST"])
def login():
    # username = None
    # password = None
    #form = LoginForm()
    #if form.validate_on_submit():
    print(session.get('username'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if username == user:
            session['username'] = username
            session['csrf_token'] = uuid.uuid4().hex  # 其实不是很明白这个选项
            # 等到看csrf攻击估计就明白了
            return redirect('/')
        else:
            flash('NOT Good Name Or Password.')
            return redirect("/login")
    else:
        return render_template("login.html")


if __name__ == "__main__":
    manager.run()  # 这样就要加参数运行了。。 runserver 或者 shell
