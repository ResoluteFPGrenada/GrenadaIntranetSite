from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from WebApp.models import User, Role, Link


class NewLinkForm(FlaskForm):
    linkname = StringField('linkname',
                       validators=[DataRequired()])

    url = StringField('url',
                      validators=[DataRequired()])

    group = StringField('group',
                        validators=[DataRequired()])

    submit = SubmitField('Create Link')

    def validate_linkname(self, linkname):
        link = Link.query.filter_by(linkname=linkname.data).first()
        if link:
            raise ValidationError('That link name is already taken. Please select another one.')

    def validate_url(self, url):
        link = Link.query.filter_by(url=url.data).first()
        if link:
            raise ValidationError('That link url is already taken. Please select another one.')


class DataSetForm(FlaskForm):
    dataType = StringField('Data Type',
                           validators=[DataRequired()])

    dataFileLocation = StringField('Data File Location',
                                   validators=[DataRequired()])

    submit = SubmitField('Create Data Set')
