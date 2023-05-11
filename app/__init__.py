from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager
from flask_mail import *
from random import randint

app = Flask(__name__)
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'phi.nqa.61cntt@ntu.edu.vn'
app.config['MAIL_PASSWORD'] = '225767322'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.secret_key = 'ashdasofaias726312=ue87105t91k&#)%'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root123@localhost/banhang?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8
mail = Mail(app)
otp = randint(000000, 999999)

db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name='djni5ipfm',
    api_key='141348169611382',
    api_secret='CDgwyvLLoWzcyHtw1NMSO7CY8u8'
)

login = LoginManager(app=app)