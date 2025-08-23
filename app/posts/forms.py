# forms.py - placeholder for acadlinker/app/posts/
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    file = FileField('Attach File', validators=[
        FileAllowed(['jpg', 'png', 'pdf', 'zip', 'txt', 'py', 'cpp', 'docx'], 'Files only!')
    ])
    submit = SubmitField('Post')
