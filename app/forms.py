from app import app
from flask_wtf import FlaskForm
from app.models import Category
from wtforms import StringField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class ArticleFrm(FlaskForm):
    title = StringField('Type Article Title', validators=[DataRequired()])
    cat_name = SelectField('Επιλογή Κατηγορίας',choices=[(category.id,category.category_name) for category in Category.query.all()], coerce=int)
    articleCont = CKEditorField('Type The Article Content')
    articleImg = FileField('ArticleImg')
    saveArticle = SubmitField('Post Article')

class CatFrm(FlaskForm):
    categoryName = StringField('Type Category Name', validators=[DataRequired()])
    saveCat = SubmitField('Add Category')