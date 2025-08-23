from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed

class MessageForm(FlaskForm):
    content = TextAreaField('Message')
    file = FileField('Attach File', validators=[FileAllowed(['jpg', 'png', 'pdf', 'txt', 'zip', 'py', 'cpp'])])
    submit = SubmitField('Send')
