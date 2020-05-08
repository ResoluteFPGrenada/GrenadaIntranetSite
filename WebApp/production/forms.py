from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, TextAreaField)
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Length, ValidationError
import datetime

class AECommentsForm(FlaskForm):
    general = TextAreaField('General')

    safety = TextAreaField('Safety')

    environment = TextAreaField('Environment')

    quality = TextAreaField('Quality / Paper Loss')

    downtime = TextAreaField('Downtime / Loss Time')

    pm = TextAreaField('Paper Machine')

    tmp = TextAreaField('TMP')

    utilities = TextAreaField('Utilities')

    woodyard = TextAreaField('Woodyard')

    customer_service = TextAreaField('Costumer Service')

    fs = TextAreaField('Finishing and Shipping')

    inventory = TextAreaField('Inventory')

    submit = SubmitField('Submit')


class MillLogForm(FlaskForm):
    date = DateField('Event Date ( in IE YYYY-MM-DD or Chrome use Date Picker)',
                     format='%Y-%m-%d')

    time = TimeField('Event Time ( in IE HH:MM or Chrome HH:MM PM)',
                     format='%H:%M')

    supervisor = SelectField('Supervisor',
                             coerce=int,
                             validators=[DataRequired()])

    e_location = SelectField('Event Location',
                             coerce=int,
                             validators=[DataRequired()])

    e_type = SelectField('Event Area',
                        coerce=int,
                        validators=[DataRequired()])

    comment = TextAreaField('Comment',
                            validators=[DataRequired()])

    submit = SubmitField('Submit')


       


