import datetime
from datetime import timedelta, datetime
from WebApp.maint.sqlite_tool import sqlite_api

db = "./app/WebApp/databases/equipment.db"

def get_new_due_date(ff, fn):
    if ff == "days":
        calc = fn
    elif ff == "weeks":
        calc = fn * 7
    elif ff == "months":
        calc = fn * 30
    elif ff == "years":
        calc = fn * 365
    else:
        return None
    new_date = datetime.today() + timedelta(days=calc)
    date = new_date.strftime('%Y-%m-%d')
    
    return date

def filter_tasks(value):
    
    #get Today date
    now = datetime.today().strftime('%Y-%m-%d')
    current_date = now

    #get Tomorrow date
    tomorrow = datetime.today() + timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')

    # query based on value given
    if value == "Past Due":
        sql = """ SELECT * FROM tasks WHERE date_due < '{}' """.format(now)
    elif value == "Today":
        sql = """ SELECT * FROM tasks WHERE date_due == '{}' """.format(now)
    elif value == "Tomorrow":
        sql = """ SELECT * FROM tasks WHERE date_due == '{}' """.format(tomorrow)
    elif value == "This Week":
        sql = """ """
    elif value == "Next Week":
        sql = """ """
    elif value == "Next Outage":
        sql = """  """
    elif value == "Annual":
        sql = """  """
    elif value == "All":
        sql = """ SELECT * FROM tasks """

    tasks = sqlite_api(db, sql, 'read')

    return tasks

def filter_objects(objects, link_id, diff_objects):
    objs = []
    filtered_objs = []
    for obj in objects:
        obj_id = obj[link_id]
        sql = """ SELECT * FROM {} WHERE id == {} """.format(diff_objects, obj_id)
        need_objs = sqlite_api(db, sql, 'read')
        for need_o in need_objs:
            if need_o not in objs:
                objs.append(need_o)
    
    return objs

def combine_objects(objects, link_id, diff_objects, combine_name):
    output_objs = []
    for diff_obj in diff_objects:
        diff_obj[combine_name] = []
        for obj in objects:
            if diff_obj['id'] == obj[link_id]:
                if obj not in diff_obj[combine_name]:
                    diff_obj[combine_name].append(obj)
                    if diff_obj not in output_objs:
                        output_objs.append(diff_obj)
    return output_objs
