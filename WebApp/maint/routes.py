from flask import (render_template, url_for, flash, redirect,
                   request, Blueprint, jsonify, abort, request)
from operator import itemgetter
import datetime
from datetime import timedelta, datetime
from WebApp.maint.utils import (filter_tasks,
                                filter_objects,
                                combine_objects,
                                get_new_due_date)
from WebApp.maint.forms import (ItemForm, AreaForm, EquipmentForm, TaskForm)
from WebApp.maint.sqlite_tool import sqlite_api
from flask_login import current_user, login_required
from WebApp.models import User, Role
from WebApp import db


maint = Blueprint('maint', __name__)
task_db = "./app/WebApp/databases/equipment.db"


@maint.route('/maint/tasks', methods=('GET', 'POST'))
@login_required
def task_manage():
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)
    return render_template('maint/tasks.html', title='Task Manage')

@maint.route('/tasks/complete/<int:task_id>')
@login_required
def complete_tasks(task_id):
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)
            
    today = datetime.today().strftime('%Y-%m-%d')
    sql = """ SELECT frequency_number, frequency_format from tasks WHERE id='{}' """.format(task_id)
    adjust_date = sqlite_api(task_db, sql, 'read')
    fn = adjust_date[0]['frequency_number']
    ff = adjust_date[0]['frequency_format']
    due_date = get_new_due_date(ff,fn)
    print(ff)
    if due_date == None:
        abort(403)

    sql = """ UPDATE tasks SET date_completed = '{}', date_due = '{}' WHERE id='{}' """.format(today, due_date, task_id)
    sqlite_api(task_db, sql, 'write')
    
    flash('Task Completed','success')
    return redirect(url_for('maint.task_manage'))


    #ITEMS SECTION#
@maint.route('/tasks/new/item', methods=('GET','POST'))
@login_required
def new_item():
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)
                
    form = ItemForm()
    
    sql = """ SELECT * FROM equipment """
    equipment = sqlite_api(task_db, sql, 'read')
    equipment = sorted(equipment, key=itemgetter('title'))
    if request.method == "GET":
        form.equipment.choices = [(int(equip['id']), equip['title']) for equip in equipment]
    elif request.method == "POST":
        name = form.name.data
        lubricant = form.lubricant.data
        points = int(form.points.data)
        equipment = form.equipment.data

        sql = """ INSERT INTO items(name, lubricant, points, equip_id)VALUES('{}','{}',{},{}) """.format(name,lubricant,points,equipment)
        sqlite_api(task_db, sql, 'write')

        flash('Your Item has been created','success')
        return redirect(url_for('maint.task_manage'))
    return render_template('maint/new_item.html', form=form, legend="Create Item", title="Create Item")

@maint.route('/tasks/update/item/<int:item_id>', methods=('GET','POST'))
@login_required
def update_item(item_id):
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)

    form = ItemForm()
    sql = """ SELECT * FROM items WHERE id = {} """.format(item_id)
    item = sqlite_api(task_db, sql, 'read')
    item = item[0]

    sql = """ SELECT * FROM equipment """
    equipment = sqlite_api(task_db, sql, 'read')
    equipment = sorted(equipment, key=itemgetter('title'))
                
    if request.method == "GET":
        form.name.data = item['name']
        form.lubricant.data = item['lubricant']
        form.points.data = item['points']
        form.equipment.choices = [(int(equip['id']), equip['title']) for equip in equipment]
    elif request.method == "POST":
        name = form.name.data
        lubricant = form.lubricant.data
        points = int(form.points.data)
        equipment = form.equipment.data

        sql = """ UPDATE items SET name='{}', lubricant='{}', points={}, equipment='{}' WHERE id={}""".format(name, lubricant, points, equipment, item_id)
        sqlite_api(task_db, sql, 'read')

        flash('Your Item has been updated.','success')
        return redirect(url_for('maint.task_manage'))
    return render_template('/maint/new_item.html', legend='Update Item', title= "Update Item", form=form)

@maint.route('/tasks/delete/item/<int:item_id>')
def delete_item(item_id):
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)
                
    sql = """ DELETE FROM items WHERE id={} """.format(item_id)
    sqlite_api(task_db, sql, 'write')
    
    flash('You item has been removed.','success')
    return redirect(url_for('maint.task_manage'))


    #AREA SECTION#
@maint.route('/tasks/new/area', methods=('GET','POST'))
def new_area():
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)

    form = AreaForm()

    if request.method == "POST":
        name = form.name.data

        sql= """ INSERT INTO area(name) VALUES('{}') """.format(name)
        sqlite_api(task_db, sql, 'write')

        flash("Your Area has been created", 'success')
        return redirect(url_for('maint.task_manager'))
    return render_template('maint/new_area.html', form=form, legend="Create Area", title= "Create Area")

@maint.route('/tasks/update/area/<int:area_id>', methods=('GET','POST'))
@login_required
def update_area(area_id):
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)

    form = AreaForm()
    sql = """ SELECT * FROM areas WHERE id = {} """.format(area_id)
    area = sqlite_api(task_db, sql, 'read')
    area = area[0]
                
    if request.method == "GET":
        form.name.data = area['name']
    elif request.method == "POST":
        name = form.name.data

        sql = """ UPDATE areas SET name='{}'WHERE id={}""".format(name, area_id)
        sqlite_api(task_db, sql, 'read')

        flash('Your Area has been updated.','success')
        return redirect(url_for('maint.task_manage'))
    return render_template('/maint/new_area.html', legend='Update Area', title= "Update Area", form=form)


@maint.route('/tasks/delete/area/<int:area_id>')
def delete_area(area_id):
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)
                
    sql = """ DELETE FROM areas WHERE id={} """.format(area_id)
    sqlite_api(task_db, sql, 'write')
    
    flash('You area has been removed.','success')
    return redirect(url_for('maint.task_manage'))


    # EQUIPMENT SECTION #
@maint.route('/tasks/new/equipment', methods=('GET','POST'))
def new_equipment():
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)
                
    form = EquipmentForm()

    sql = """ SELECT * FROM areas """
    areas = sqlite_api(task_db, sql, 'read')
    areas = sorted(areas, key=itemgetter('name'))
    
    if request.method == "GET":
        form.area.choices = [(int(area['id']), area['name']) for area in areas]
    elif request.method == "POST":
        title = form.title.data
        area = form.area.data

        sql = """ INSERT INTO equipment(title, area_id)VALUES('{}',{}) """.format(title, area)
        sqlite_api(task_db, sql, 'write')

        flash('Your Equipment has been created','success')
        return redirect(url_for('maint.task_manage'))
    return render_template('maint/new_equipment.html', form=form, legend="Create Equipment", title="Create Equipment")

@maint.route('/tasks/update/equipment/<int:equip_id>', methods=('GET','POST'))
@login_required
def update_equipment(equip_id):
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)

    form = EquipmentForm()
    sql = """ SELECT * FROM equipment WHERE id = {} """.format(equip_id)
    equipment = sqlite_api(task_db, sql, 'read')
    equipment = equipment[0]

    sql = """ SELECT * FROM areas """
    areas = sqlite_api(task_db, sql, 'read')
    areas = sorted(areas, key=itemgetter('name'))
                
    if request.method == "GET":
        form.title.data = equipment['title']
        form.area.choices = [(int(area['id']), area['name'])for area in areas]
    elif request.method == "POST":
        title = form.title.data
        area = form.area.data
    
        sql = """ UPDATE equipment SET title='{}', area_id={} WHERE id={}""".format(title, area, equip_id)
        sqlite_api(task_db, sql, 'read')

        flash('Your Equipment has been updated.','success')
        return redirect(url_for('maint.task_manage'))
    return render_template('/maint/new_equipment.html', legend='Update Equipment', title= "Update Equipment", form=form)


@maint.route('/tasks/delete/equipment/<int:equipment_id>')
def delete_equipment(equip_id):
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)
                
    sql = """ DELETE FROM equipment WHERE id={} """.format(equip_id)
    sqlite_api(task_db, sql, 'write')
    
    flash('You equipment has been removed.','success')
    return redirect(url_for('maint.task_manage'))


    #TASK SECTION#
@maint.route('/tasks/new/task', methods=('GET', 'POST'))
def new_task():
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)

    form = TaskForm()

    sql = """ SELECT * FROM items """
    items = sqlite_api(task_db, sql, 'read')
    items = sorted(items, key=itemgetter('name'))

    if request.method == "GET":
        form.item.choices = [(int(item['id']), item['name']) for item in items]
        form.frequencyFormat.choices = [(0,"days"), (1,"weeks"), (2,"months"), (3,"years")]
    elif request.method == "POST":
        name = form.name.data
        item = form.item.data
        dateDue = form.DateDue.data
        freqNumber = form.frequencyNumber.data
        freqFormat = form.frequencyFormat.data

        if freqFormat == 0:
            freqFormated = 'days'
        elif freqFormat == 1:
            freqFormated = 'weeks'
        elif freqFormat == 2:
            freqFormated = 'months'
        elif freqFormat == 3:
            freqFormated = 'years'

        sql = """ INSERT INTO tasks(name, item_id,
date_due, frequency_number,
frequency_format)VALUES('{}',{},'{}',{},'{}') """.format(name,item,
                                                         dateDue,freqNumber,
                                                         freqFormated)
        sqlite_api(task_db, sql, 'write')

        flash('Your task has been created','success')
        return redirect(url_for('maint.task_manage'))
    return render_template('maint/new_task.html', form=form, legend="Create Task", title="Create Task")

@maint.route('/tasks/update/task/<int:task_id>', methods=('GET','POST'))
@login_required
def update_task(task_id):
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)

    form = TaskForm()
    sql = """ SELECT * FROM tasks WHERE id = {} """.format(task_id)
    task = sqlite_api(task_db, sql, 'read')
    task = task[0]

    sql = """ SELECT * FROM items """
    items = sqlite_api(task_db, sql, 'read')
    items = sorted(items, key=itemgetter('name'))
                
    if request.method == "GET":
        form.name.data = task['name']
        form.item.choices = [(int(item['id']), item['name'])for item in items]
        form.DateDue.data = datetime.strptime(task['date_due'], '%Y-%m-%d')
        form.frequencyNumber.data = task['frequency_number']
        form.frequencyFormat.choices = [(0,"days"),(1,"weeks"), (2,"months"),(3,"yeas")]
        form.frequencyFormat.data = task['frequency_format']
    elif request.method == "POST":
        name = form.name.data
        item = form.item.data
        dateDue = form.DateDue.data
        freqNumber = form.frequencyNumber.data
        freqFormat = form.frequencyFormat.data

        if freqFormat == 0:
            freqFormated = 'days'
        elif freqFormat == 1:
            freqFormated = 'weeks'
        elif freqFormat == 2:
            freqFormated = 'months'
        elif freqFormat == 3:
            freqFormated = 'years'

    
        sql = """ UPDATE tasks SET name='{}', item_id={},
            date_due='{}', frequency_number={},
            frequency_format='{}' WHERE id={}""".format(name, item,
                                                        dateDue, freqNumber,
                                                        freqFormated, task_id)
        sqlite_api(task_db, sql, 'read')

        flash('Your Task has been updated.','success')
        return redirect(url_for('maint.task_manage'))
    return render_template('/maint/new_task.html', legend='Update Task', title= "Update Task", form=form)

@maint.route('/tasks/delete/task/<int:task_id>')
def delete_task(task_id):
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
            if not 'Maintenance' in rights:
                abort(403)
                
    sql = """ DELETE FROM tasks WHERE id={} """.format(task_id)
    sqlite_api(task_db, sql, 'write')
    
    flash('You task has been removed.','success')
    return redirect(url_for('maint.task_manage'))
    

@maint.route('/tasks/<string:value>/json')
#@login_required
def json_tasks(value):
    tasks = []
    items = []
    output_items = ""
    equipment = []
    output_equipment = ""
    areas = []
    output_areas = ""
    # add credential code later

    
    tasks = filter_tasks(value)
    tasks = sorted(tasks, key=itemgetter('name'))
    # filter objects based on tasks and the value for the query
    
    
    items = filter_objects(tasks, "item_id", 'items')
    items = sorted(items, key=itemgetter('name'))
    
    equipment = filter_objects(items, 'equip_id', 'equipment')
    equipment = sorted(equipment, key=itemgetter('title'))
    
    areas = filter_objects(equipment, 'area_id', 'areas')
    areas = sorted(areas, key=itemgetter('name'))

    # combine objects based on secondary id
    output_items = combine_objects(tasks, 'item_id', items, 'tasks')
    output_equipment = combine_objects(output_items, 'equip_id', equipment, 'items')
    output_areas = combine_objects(output_equipment, 'area_id', areas, 'equipment')
    
    return jsonify(output_areas)

@maint.route('/maint/personnel_training')
@login_required
def personnel_training():
    if not current_user.is_admin:
        user = User.query.filter_by(id=current_user.id).first()
        rights = [right.group for right in user.rights]
        if not 'MaintAdmin' in rights:
                abort(403)
    return render_template('/maint/personnel_training.html', title="Personnel Training")
    


