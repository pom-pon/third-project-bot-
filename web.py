from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


# Configure application
app = Flask(__name__)


@app.route("/")
@app.route("/web.html")
def get_index():
    return render_template('web.html')


@app.route("/news.html")
def test_link():
    return render_template('news.html')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


#Run
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)