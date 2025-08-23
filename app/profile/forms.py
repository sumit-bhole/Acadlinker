from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Optional
from flask_wtf.file import FileAllowed

class EditProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    mobile_no = StringField('Mobile Number', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    description = TextAreaField('Bio/Description', validators=[Optional()])
    skills = StringField('Skills (comma separated)', validators=[Optional()])
    education = TextAreaField('Education', validators=[Optional()])
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    cover_photo = FileField('Cover Photo', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Profile')
