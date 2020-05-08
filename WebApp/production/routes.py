from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required
from WebApp.production.forms import (AECommentsForm, MillLogForm)
from WebApp.production.utils import send_AE_email, send_log
from WebApp.api.sqlite_tool import sqlite_api
import datetime
from datetime import timedelta, datetime

production = Blueprint('production', __name__)

@production.route('/kpi')
def kpi():
    return render_template('kpi.html')

@production.route('/kpi/new')
def kpi_new():
    return render_template('kpi_new.html')

@production.route('/mill_log')
def mill_log():
    db = "./app/WebApp/databases/logs.db"

    sql = """ SELECT * FROM MillLogs """
    logs = sqlite_api(db, sql, 'read')
    
    return render_template('production/mill_log.html', logs=logs, title="Mill Logs")

@production.route('/mill_log/update/<int:log_id>', methods=('GET','POST'))
@login_required
def mill_log_update(log_id):
    supervisors = ["",
                   "Ricky Baker",
                   "Jeff Hand",
                   "Ricky Darbonne",
                   "Darrell Reddit",
                   "Bill Lee",
                   "Herman Cummins",
                   "Mike Tipton",
                   "Tom Conte",
                   "Dan Hogan",
                   "Rob Wise"]
    locations = ["",
                 "Woodyard",
                 "Utilities",
                 "TMP",
                 "PM",
                 "Winder",
                 "F & S",
                 "Maintenance",
                 "Admin",
                 "GENERAL",
                 "MISC"]
    types = ["",
             "SAFETY",
             "NEAR MISS",
             "HAZARD",
             "MECHANICAL",
             "ELECTRICAL",
             "WEATHER",
             "COMMUNICATION",
             "PROCESS",
             "MISC"]

    db = "./app/WebApp/databases/logs.db"
    sql = """ SELECT * FROM MillLogs WHERE id = {} """.format(log_id)
    log = sqlite_api(db, sql, 'read')
    log = log[0]
    form = MillLogForm()

    if request.method == "GET":
        form.date.data = datetime.strptime(log['date'], '%Y-%m-%d')
        form.time.data = datetime.strptime(log['time'], '%H:%M:%S')
        form.supervisor.choices = [(supervisors.index(supervisor), supervisor) for supervisor in supervisors]
        form.supervisor.data = supervisors.index(log['supervisor'])
        form.e_location.choices = [(locations.index(location), location) for location in locations]
        form.e_location.data = locations.index(log['location'])
        form.e_type.choices = [(types.index(e_type), e_type) for e_type in types]
        form.e_type.data = types.index(log['type'])
        form.comment.data = log['comment']
    elif request.method == "POST":
        if form.date.data == None:
            flash('Please enter correct date format','danger')
            return redirect(url_for('production.mill_log_update', log_id=log_id))
        if form.time.data == None:
            flash('Please eneter correct time format','danger')
            return redirect(url_for('production.mill_log_update', log_id=log_id))

        username = current_user.username
        date = str(form.date.data)
        time = str(form.time.data)
        supervisor = supervisors[form.supervisor.data]
        e_location = locations[form.e_location.data]
        e_type = types[form.e_type.data]
        comment = (form.comment.data).replace('”', '"')
        comment = comment.replace('“', '"')
        comment = comment.replace("’", "'")
        comment = comment.replace("'", "''")

        sql = """ UPDATE MillLogs
SET date = '{}', time = '{}', supervisor = '{}', location = '{}', type = '{}', comment = '{}'
WHERE id={}""".format(date,
                      time,
                      supervisor,
                      e_location,
                      e_type,
                      comment,
                      log_id)
        sqlite_api(db, sql, 'write')
        now_log = datetime.now()
        send_log(f'{current_user.username}, updated log with ID: {log_id}, {now_log}', 'MillLogActivity')

    
        flash('This log has been updated','success')
        return redirect(url_for('production.mill_log'))
    return render_template('production/mill_log_update.html',form=form, title="Update Mill Log", legend="Update Log")

@production.route('/mill_log/delete/<int:log_id>', methods=('GET','POST'))
@login_required
def mill_log_delete(log_id):
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'Production' in rights:
            abort(403)
    
    db = "./app/WebApp/databases/logs.db"
    sql = """ DELETE FROM MillLogs WHERE id = {} """.format(log_id)
    sqlite_api(db, sql, 'write')
    
    flash('This log has been deleted','success')
    return redirect(url_for('production.mill_log'))

@production.route('/mill_log/new',methods=('GET','POST'))
@login_required
def mill_log_new():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    
    db = "./app/WebApp/databases/logs.db"
    form = MillLogForm()
    supervisors = ["",
                   "Ricky Baker",
                   "Jeff Hand",
                   "Ricky Darbonne",
                   "Darrell Reddit",
                   "Bill Lee",
                   "Herman Cummins",
                   "Mike Tipton",
                   "Tom Conte",
                   "Dan Hogan",
                   "Rob Wise"]
    locations = ["",
                 "Woodyard",
                 "Utilities",
                 "TMP",
                 "PM",
                 "Winder",
                 "F & S",
                 "Maintenance",
                 "Admin",
                 "GENERAL",
                 "MISC"]
    types = ["",
             "SAFETY",
             "NEAR MISS",
             "HAZARD",
             "MECHANICAL",
             "ELECTRICAL",
             "WEATHER",
             "COMMUNICATION",
             "PROCESS",
             "MISC"]

    if request.method =='GET':
        pass
        #form.supervisor.choices = [(supervisors.index(supervisor),supervisor) for supervisor in supervisors]
        #form.e_location.choices = [(locations.index(location),location) for location in locations]
        #form.e_type.choices = [(types.index(e_type), e_type) for e_type in types]

    form.supervisor.choices = [(supervisors.index(supervisor),supervisor) for supervisor in supervisors]
    form.e_location.choices = [(locations.index(location),location) for location in locations]
    form.e_type.choices = [(types.index(e_type), e_type) for e_type in types]

    if form.validate_on_submit():
        

            # Gather data and enter into database.
        username = current_user.username
        date = str(form.date.data)
        time = str(form.time.data)
        supervisor = supervisors[form.supervisor.data]
        e_location = locations[form.e_location.data]
        e_type = types[form.e_type.data]
        comment = form.comment.data
        comment = comment.replace('”', '"')
        comment = comment.replace('“', '"')
        comment = comment.replace("’", "'")
        comment = comment.replace("'", "''")


        sql = """ INSERT INTO MillLogs (user, date, time, supervisor, location, type, comment)
VALUES('{}','{}','{}','{}','{}','{}','{}');""".format(username, date, time, supervisor, e_location, e_type, comment)

        sqlite_api(db, sql, 'write')

            # Send log.
        now_log = datetime.now()
        send_log(f'{current_user.username}, created log, {now_log}', 'MillLogActivity')


        flash("Your log has been saved","success")
        return redirect(url_for('production.mill_log'))
    return render_template('production/mill_log_new.html', form=form, title="New Mill Log", legend="Create Log")

@production.route('/rcpe')
def rcpe():
    return render_template('rcpe.html')

@production.route('/rcpe/new')
def rcpe_new():
    return render_template('rcpe_new.html')

@production.route('/action_items')
def action_items():
    return render_template('action_items.html')

@production.route('/ae_comments', methods=('GET','POST'))
def ae_comments():
    form = AECommentsForm()

    if request.method == 'POST':
        
        data = {
            'general' : form.general.data,
            'safety' : form.safety.data,
            'environment' : form.environment.data,
            'quality' : form.quality.data,
            'downtime' : form.downtime.data,
            'pm' : form.pm.data,
            'tmp' : form.tmp.data,
            'utilities' : form.utilities.data,
            'woodyard' : form.woodyard.data,
            'customer_service' : form.customer_service.data,
            'fs' : form.fs.data,
            'inventory' : form.inventory.data
        }
        
        # send email
        send_AE_email(data)
        
        flash('Your comments were sent to be reviewed.', 'success')
        return redirect(url_for('main.home'))
    return render_template('production/ae_comments_new.html', title="AE Comments", legend="Enter AE Comments", form=form)


