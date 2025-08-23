# forms.py - placeholder for acadlinker/app/groups/
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CreateGroupForm(FlaskForm):
    title = StringField('Group Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('Create Group')
