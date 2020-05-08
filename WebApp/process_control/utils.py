import os
import secrets
from PIL import Image
from flask import url_for, current_app

def send_log(message, log_type):
    log_path = os.path.join(current_app.root_path, 'static/logs/', log_type + '.log')
    file = open(log_path, 'a')
    file.write(message)
    file.write(os.linesep)
    file.close()

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/InventoryPics", picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def delete_picture(form_picture):
    picture_path = os.path.join(current_app.root_path, "static/InventoryPics", form_picture)
    os.remove(picture_path)

def filter_attributes(objects, attribute):
    props = []

    for obj in objects:
        prop = obj[attribute]
        if prop not in props:
            props.append(prop)

    return props

def filter_objects(objects, attribute, item_filter):
    objs = []
    for obj in objects:
        props = []
        props = [obj[attribute] for obj in objs]
        if obj[attribute] == item_filter and item_filter not in props:
            objs.append(obj)

    return objs
