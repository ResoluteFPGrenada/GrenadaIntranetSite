from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                     SelectField, SelectMultipleField, TextAreaField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from WebApp.models import User, Role, Link



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    admin = BooleanField('Administrator')

    password = PasswordField('Password',
                             validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

        # custom validators
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is take. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is take. Please choose a different one.')

class RoleForm(FlaskForm):
    group = StringField('group',
                        validators=[DataRequired()])

    description = TextAreaField('description',
                              validators=[DataRequired()])

    submit = SubmitField('Create Role')

    def validate_group(self, group):
        role = Role.query.filter_by(group=group.data).first()
        if role:
            raise ValidationError('That group name is already taken. Please select another one.')

class PermissionForm(FlaskForm):
    username = SelectField(u'username', coerce=int, validators=[DataRequired()])
    
    roles = SelectMultipleField(u'roles', coerce=int, validators=[])
    
    assigned = SelectMultipleField(u'assigned', coerce=int, validators=[])

    submit = SubmitField('Update Permissions')

class RoleModForm(FlaskForm):
    group = SelectField('group',
                        validators=[])

    description = TextAreaField('description',
                              validators=[DataRequired()])

    submit = SubmitField('Update Role')

class NewLinkForm(FlaskForm):
    linkname = StringField('linkname',
                       validators=[DataRequired()])

    url = StringField('url',
                      validators=[DataRequired()])

    group = StringField('group',
                        validators=[DataRequired()])

    submit = SubmitField('Submit')

    def validate_linkname(self, linkname):
        link = Link.query.filter_by(linkname=linkname.data).first()
        if link:
            raise ValidationError('That link name is already taken. Please select another one.')

    def validate_url(self, url):
        link = Link.query.filter_by(url=url.data).first()
        if link:
            raise ValidationError('That link url is already taken. Please select another one.')

class UpdateLinkForm(FlaskForm):
    linkname = StringField('linkname',
                       validators=[DataRequired()])

    url = StringField('url',
                      validators=[DataRequired()])

    group = StringField('group',
                        validators=[DataRequired()])

    submit = SubmitField('Submit')

