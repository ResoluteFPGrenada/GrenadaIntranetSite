from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField,
                    IntegerField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, ValidationError

class ItemForm(FlaskForm):
    name = StringField('Name',
                       validators =[DataRequired()])

    lubricant = StringField('Lubricant',
                            validators=[DataRequired()])

    points = StringField('Points',
                         validators=[DataRequired()])

    equipment = SelectField(u'Equipment',
                            coerce=int,
                            validators=[DataRequired()])

    submit = SubmitField('Submit')


class AreaForm(FlaskForm):
    name = StringField('Name',
                       validators= [DataRequired()])

    submit = SubmitField('Submit')

class EquipmentForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])

    area = SelectField('Area',
                       coerce=int,
                       validators=[DataRequired()])

    submit = SubmitField('Submit')

class TaskForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired()])

    item = SelectField('Item',
                       coerce=int,
                       validators=[DataRequired()])

    DateDue = DateField('Date Due',
                        format='%Y-%m-%d',
                        validators=[DataRequired()])

    frequencyNumber = IntegerField('Frequency Number',
                                   validators=[DataRequired()])

    frequencyFormat = SelectField('Frequency Format',
                                  coerce=int,
                                  validators=[DataRequired()])

    submit = SubmitField('Submit')

