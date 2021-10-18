from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
import os

baseDir = os.path.abspath(os.path.dirname(__file__)) #'/home/tinos/Trainig/Python/senn-dev/app/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fa1f944ab8bd63090d9d4bc945bc0dfd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(baseDir, 'senn.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLODED_IMAGES_DEST'] = 'upimages/'
app.config['ALLOW_IMG_EXT'] = ['gif', 'jpg', 'jpeg', 'png']

db = SQLAlchemy(app)
ckeditor = CKEditor(app)

app.config['CKEDITOR_HEIGHT'] = 600
app.config['CKEDITOR_PKG_TYPE'] = 'basic'

from app import routes