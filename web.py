from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import smtplib
import mimetypes
from email.mime.multipart import MIMIMultipart
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import sqlite3
import os


SECRET_KEY = 'yandexlyceum_secret_key'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap4(app)
load_dotenv()


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

@app.route('/email.html', method=['GET'])
def get_form():
    return render_template('email.html')


def send_email(email, subject, text, attachments):
    addr_form = os.getenv('FROM')
    password = os.getenv('PASSWORD')
    msg = MIMIMultipart()
    msg['From'] = addr_form
    msg['To'] = email
    msg['Subject'] = subject
    body = text
    msg.attach(MIMEText(body, 'plain'))
    process_attachements(msg, attachments)
    server = smtplib.SMTP_SSL(os.getenv('HOST'), os.getenv('PORT'))
    server.send_message(msg)
    server.quit()
    return True


def process_attachements(msg, attachments):
    for f in attachments:
        if os.path.isfile(f):
            attach_file(msg, f)
        elif os.path.exists(f):
            dir = os.listdir(f)
            for file in dir:
                attach_file(msg, f + '/' + file)


def attach_file(msg, f):
    attach_types = {
        'text': MIMEText,
        'image': MIMEImage,
        'audio': MIMEAudio
    }
    filename = os.path.basename(f)
    ctype, encoding = mimetypes.guess_type(f)
    if ctype is None or encoding is not None:
        ctype == 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    with open(f, mode='rb' if maintype != 'text' else 'r') as fp:
        if maintype in attach_types:
            file = attach_types[maintype](fp.read(), _subtype=subtype)
        else:
            file = MIMEBase(maintype, subtype)
            file.set_payload(fp.read())
            encoders.encode_base64(file)
        file.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(file)

@app.route('/email.html', method=['POST'])
def post_form():
    email = request.values('email')
    if send_email(email, 'текстовое письмо', 'текст', ['picture.png', 'pdfdoc.pdf', 'text.txt']):
        return 'Письмо отправлено успешно'
    return 'Возникла ошибка, письмо не отправлено'


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