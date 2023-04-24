from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
import sqlite3
import os


SECRET_KEY = 'yandexlyceum_secret_key'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap4(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studying = db.Column(db.String(100), nullable= False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    patronymic = db.Column(db.String(100), nullable=False)
    clas = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    five = db.Column(db.Integer, primary_key=False)
    four = db.Column(db.Integer, primary_key=False)
    three = db.Column(db.Integer, primary_key=False)
    two = db.Column(db.Integer, primary_key=False)
    concerts = db.Column(db.String(100), nullable=False)
    achievements = db.Column(db.String(100), nullable=False)
    goverment = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route("/")
@app.route("/web.html")
def get_index():
    return render_template('web.html')


@app.route("/base.html", methods=['POST', 'GET'])
def base():
    if request.method == "POST":
        studying = request.form['studying']
        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']
        clas = request.form['clas']
        username = request.form['username']
        five = request.form['five']
        four = request.form['four']
        three = request.form['three']
        two = request.form['two']
        concerts = request.form['concerts']
        achievements = request.form['achievements']
        goverment = request.form['goverment']
        article = Article(studying=studying, name=name, surname=surname, patronymic=patronymic, clas=clas,
                          username=username, five=five, four=four, three=three, two=two, concerts=concerts,
                          achievements=achievements, goverment=goverment)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/web.html')
        except:
            return 'При занесении новых данных произошла ошибка'
    return render_template('base.html')


@app.route("/news.html")
def test_link():
    return render_template('news.html')


@app.route("/rating.html")
def rating():
    articles = Article.query.all()
    return render_template('rating.html', articles=articles)


#Run
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)