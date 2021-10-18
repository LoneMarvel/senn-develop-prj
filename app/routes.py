from logging import FileHandler, LogRecord
from flask import render_template, url_for, redirect, request
from app import app
from app import db
from app.models import Profile, Members, Articles, Category
from app.forms import ArticleFrm, CatFrm
from werkzeug.utils import secure_filename
from datetime import datetime
import os

baseDir = os.path.abspath(os.path.dirname(__file__)) #'/home/tinos/Trainig/Python/senn-dev/app/'

@app.route('/')
def Index():
    
    pageData = {
        'pageTitle':'Σωματείο Εργαζομένων Νοσοκομείου Νάουσας To Προφιλ Του Σωματίου',        
        'profileData':Profile.query.first()
    }
    return render_template('profile.html',pageData=pageData)

@app.route('/articles')
def DisplayArticles():
    pageNum = request.args.get('pageNum', type=int)
    perPage = 4
    articlesList = Articles.query.paginate(pageNum,perPage)
    return render_template('articlesmain.html',articlesList=articlesList)

@app.route('/adm',methods=['POST','GET'])
def IndexAdm():       
    return render_template('admindex.html')

@app.route('/admarticle',methods=["POST", "GET"])
def ArticleAdm():
    noArticleMsg = 'No Articles Found . . .'        
    pageNum = request.args.get('pageNum', type=int)  
    perPage = 3
    dateIn = datetime.now()
    articleFrm = ArticleFrm()
    articlesLst = Articles.query.paginate(pageNum,perPage)     
    if articleFrm.validate_on_submit():        
        articleImgFile = secure_filename(articleFrm.articleImg.data.filename)        
        if articleImgFile == '':
            articleImgFile = url_for('static', filename='images/SennIconLogo.png')
            articleFrm.articleImg.data = articleImgFile
            saveFlag, frmData = DoSaveToDB(articleFrm)            
        else: 
            if CheckAllowImgExt(articleImgFile):                             
                articleImgFile = secure_filename(articleFrm.articleImg.data.filename)                   
                articleFrm.articleImg.data.save(baseDir+'/static/'+app.config['UPLODED_IMAGES_DEST']+articleImgFile)
                articleFrm.articleImg.data = articleImgFile
                saveFlag, frmData = DoSaveToDB(articleFrm)
                articlesLst = Articles.query.paginate(pageNum,perPage)        
            else:            
                print('File does not much with the valid extensions') 
                return render_template('admarticlesmain.html',articleFrm=articleFrm,articlesLst=articlesLst)           
        if saveFlag:
            articleFrm = frmData
            articlesLst = Articles.query.paginate(pageNum,perPage)
            saveResMsg = 'Article Saved Successfully To DB'  
        else:
            articleFrm = frmData
            saveResMsg = 'Article Did Not Saved Successfully To DB'    
        print(saveResMsg)                           
    if not articlesLst:        
        return render_template('admarticlesmain.html',articleFrm=articleFrm,noArticleMsg=noArticleMsg)      
    return render_template('admarticlesmain.html',articleFrm=articleFrm,articlesLst=articlesLst)

@app.route('/admrecarticle/<int:articleId>',methods=['POST','GET'])
def ArticleEdit(articleId):    
    pageNum = request.args.get('pageNum', type=int)  
    perPage = 3    
    dateNow=str(datetime.now()).rsplit(".")[0]                       
    updDate = datetime.strptime(dateNow,'%Y-%m-%d %H:%M:%S')
    articleFrm = ArticleFrm()
    recArticle = Articles.query.filter_by(id=articleId).first()    
    imageScr = app.config['UPLODED_IMAGES_DEST']+recArticle.article_img_name   
    if articleFrm.validate_on_submit():
        articleImgFile = secure_filename(articleFrm.articleImg.data.filename)        
        if articleImgFile == '':            
            articleImgFile = url_for('static', filename=imageScr)            
            recArticle.title = articleFrm.title.data
            recArticle.article_cat = articleFrm.cat_name.data
            recArticle.article_cont = articleFrm.articleCont.data 
            recArticle.article_date = updDate
        else: 
            if CheckAllowImgExt(articleImgFile):                                             
                articleImgFile = secure_filename(articleFrm.articleImg.data.filename)                   
                articleFrm.articleImg.data.save(baseDir+'/static/'+app.config['UPLODED_IMAGES_DEST']+articleImgFile)                
                recArticle.title = articleFrm.title.data
                recArticle.article_cat = articleFrm.cat_name.data
                recArticle.article_cont = articleFrm.articleCont.data
                recArticle.article_img_name = articleImgFile                 
                recArticle.article_date = updDate
            else:            
                print('File does not much with the valid extensions') 
                articlesLst = Articles.query.paginate(pageNum,perPage)
                return render_template('admarticlesmain.html',articleFrm=articleFrm,articlesLst=articlesLst) 
        db.session.flush()
        db.session.commit()               
        articlesLst = Articles.query.paginate(pageNum,perPage)        
        return render_template('admarticlesmain.html',articleFrm=articleFrm,articlesLst=articlesLst)
    articleFrm.articleCont.data = recArticle.article_cont
    return render_template('articlerecscreen.html',articleFrm=articleFrm,recArticle=recArticle,imageScr=imageScr)

@app.route('/admcat',methods=['POST','GET'])
def CatAdm():
    catFrm = CatFrm()
    catLst = Category.query.all()
    if catFrm.validate_on_submit():
        newCat = Category(category_name=catFrm.categoryName.data)
        db.session.add(newCat)
        db.session.commit()
        catLst = Category.query.all()
        render_template('catscreen.html',catLst=catLst,catFrm=catFrm)
    return render_template('catscreen.html',catLst=catLst,catFrm=catFrm)

@app.route('/admcatedit/<int:catId>',methods=['POST','GET'])
def CatEdit(catId):    
    print(f"Category Id Is {catId}")
    catFrm = CatFrm()
    catRec = Category.query.filter_by(id=catId).first()
    if catFrm.validate_on_submit():
        catRec.category_name = catFrm.categoryName.data
        db.session.flush()
        db.session.commit()
        catLst = Category.query.all()
        return render_template('catscreen.html',catLst=catLst,catFrm=catFrm)
    return render_template('catrecscreen.html',catRec=catRec,catFrm=catFrm)

""" 16.10.2021
Summary
-----------------------------------
Support Functions

Purpose
-----------------------------------

Return
-----------------------------------
"""
def CheckAllowImgExt(imgFileName):
    if not '.' in imgFileName:
        return False
    fileExt = imgFileName.rsplit('.',1)[1]
    if not fileExt.lower() in app.config['ALLOW_IMG_EXT']:
        return False
    return True

def DoSaveToDB(dataToSave):
    print(f"In Function And Data to Save -> {dataToSave}")
    print(f"Title -> {dataToSave.title.data}\nArticle Content -> {dataToSave.articleCont.data}\nArticle Category -> {dataToSave.cat_name.data}\nImage ->{dataToSave.articleImg.data}")
    newArticle = Articles(title=dataToSave.title.data,article_cont=dataToSave.articleCont.data,article_cat=dataToSave.cat_name.data,article_img_name=dataToSave.articleImg.data)#Save2DB                
    db.session.add(newArticle)
    db.session.commit()
    dataToSave.title.data = ''
    dataToSave.articleCont.data = ''
    dataToSave.articleImg.data = ''
    dataToSave.articleImg.data = ''
    return {True,dataToSave}
