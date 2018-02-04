from flask import Flask, render_template, \
    redirect, request, abort, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap







app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
bootstrap = Bootstrap(app)

@app.route('/')
def index():

    name = 'immcy'
    if 'name' in session:
        name = session['name']

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
    if request.method == 'POST':
        username = request.form.get('username')
        print(username)

        password = request.form.get('password')
        print(password)
        if username == 'wy' and password == '123':
            session['name'] = username
            return redirect('/')
        else:
            flash('NOT Good Name Or Password.')
            return redirect("/login")
    else:
        return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True, port=9000)