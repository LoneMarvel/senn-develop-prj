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
