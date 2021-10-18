from app import db
from datetime import datetime

class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    profile_txt = db.Column(db.Text())

    def __init__(self,title,profile_txt):
        self.title = title
        self.profile_txt = profile_txt

class Members(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120),nullable=False)
    email = db.Column(db.String(120),nullable=False)

    def __init__(self,fullname,email):
        self.fullname - fullname
        self.email = email

class Articles(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    article_cont = db.Column(db.Text())
    article_cat = db.Column(db.Integer,db.ForeignKey('category.id'))
    article_img_name = db.Column(db.String(255))
    article_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    #def __init__(self,title,article_cont,article_cat,article_img_name):
    #    self.title = title
    #    self.article_cont = article_cont
    #    self.article_cat = article_cat
    #    self.article_img_name = article_img_name
        #self.article_date = article_date        

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer,primary_key=True)
    category_name = db.Column(db.String(255),nullable=False)
    articles_cat = db.relationship('Articles',backref='artcat',lazy='select')

    def __init__(self,category_name):
        self.category_name = category_name

    def CategoryList(self):
        return Category.query.all()
        


