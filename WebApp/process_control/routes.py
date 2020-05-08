from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import current_user, login_required
from WebApp.process_control.forms import (InventoryForm, InventoryUpdateForm, InventoryQuestionareForm)
from WebApp.api.sqlite_tool import sqlite_api
from WebApp.process_control.utils import (save_picture, delete_picture, send_log, filter_attributes, filter_objects)
import datetime
from datetime import timedelta, datetime
import json
import os

process_control = Blueprint('process_control', __name__)
db = "./app/WebApp/databases/inventory.db"

#IVENTORY#
@process_control.route('/pc/inventory')
@login_required
def inventory_pc():
    user_id = current_user.id
    
    inventory = []
    cart = []

    #get data from database#
    sql = """ SELECT * FROM Cart WHERE userId = {} """.format(user_id)
    cart = sqlite_api(db, sql, "read")
    
    sql = """ SELECT * FROM Inventory """
    inventory = sqlite_api(db, sql, "read")
    manufacturers = filter_attributes(inventory, "manufacturer")
    models = filter_attributes(inventory, "model")
    categories = filter_attributes(inventory, "category")
    ref_items = filter_attributes(inventory, "refItem")
    
    return render_template('process_control/inventory.html',
                           manufacturers = manufacturers,
                           models = models,
                           inventory = inventory,
                           ref_items = ref_items,
                           categories = categories,
                           cart = cart)

#CHECKOUT#
@process_control.route("/pc/inventory/cart/checkout")
@login_required
def inventory_cart_checkout():
    user_id = current_user.id
    sql = """ SELECT * FROM Cart WHERE userId = '{}' """.format(user_id)
    cart = sqlite_api(db, sql, 'read')
    item_ids = [item["inventoryId"] for item in cart]

    sql = """ SELECT * FROM Inventory WHERE""".format(user_id)
    for item in item_ids:
        if sql == """ SELECT * FROM Inventory WHERE""".format(user_id):
            sql = sql + " id = '{}'".format(item)
        else:
            sql = sql + " or id = '{}'".format(item)
    items = sqlite_api(db, sql, 'read')
    

    return render_template("process_control/checkout.html", cart=cart, items=items)

#COMPLETE CHECKOUT#
@process_control.route("/pc/inventory/cart/completeCheckout/<jsonObj>")
@login_required
def inventory_cart_completeCheckout(jsonObj):
    #GET DATA FROM DATABASE#
    sql = """ SELECT * FROM Inventory """
    
    objs = json.loads(jsonObj)
    for obj in objs:
        if sql == """ SELECT * FROM Inventory """:
            sql = sql + "WHERE id = '{}'".format(obj["itemId"])
        else:
            sql = sql + " or id = '{}'".format(obj["itemId"])

    items = sqlite_api(db, sql, 'read')

        #GET NEW QUANTITIES#
    data = []
    for obj in objs:
        for item in items:
            
            if int(obj["itemId"]) == item["id"]:
                
                #Compile data for retrieval#
                d = {
                    'itemName' : item['itemName'],
                    'rQuantity' : obj['quantity'],
                    'itemLocation' : item['locationId']
                    }
                data.append(d)
                
                #UPDATE DATABASE#
                new_quantity = item['quantity'] - int(obj["quantity"])
                sql = """ UPDATE Inventory SET quantity = '{}' WHERE id = '{}'""".format(new_quantity, item['id'])
                sqlite_api(db, sql, 'write')

                #REMOVE items from cart#
                sql = """ DELETE FROM cart WHERE userId = '{}' """.format(current_user.id)
                sqlite_api(db, sql, 'write')

    flash("Your items have been removed from inventory.","success")
    return render_template("process_control/inventory_retrieve_items.html", data = data)
    

#REMOVE ITEM FROM CART#
@process_control.route("/pc/inventory/cart/remove/<int:item_id>")
@login_required
def inventory_cart_remove(item_id):
    user_id = current_user.id
    sql = """ SELECT * FROM cart WHERE userId = '{}' """.format(user_id)
    user_cart = sqlite_api(db, sql, "read")
    item_ids = [item["inventoryId"] for item in user_cart]
    if item_id not in item_ids:
        flash("This item was not in your cart.","danger")
        return redirect(url_for("process_control.inventory_pc"))

    sql = """ DELETE FROM Cart WHERE userId = '{}' and inventoryId = '{}' """.format(user_id, item_id)
    sqlite_api(db, sql, 'write')

    flash("This item has been removed from your cart.", "success")
    return redirect(url_for('process_control.inventory_pc'))
    
        

#ADD ITEM TO CART#
@process_control.route("/pc/inventory/cart/<int:item_id>")
@login_required
def inventory_cart(item_id):
    user_id = current_user.id
    sql = """ SELECT * FROM cart WHERE userId = '{}' """.format(user_id)
    user_cart = sqlite_api(db, sql, "read")
    for item in user_cart:
        if item["inventoryId"] == item_id:
            flash("This item is already in your cart","danger")
            return redirect(url_for("process_control.inventory_pc"))
    
    sql = """ INSERT INTO cart (userId, InventoryId)
    VALUES ('{}', '{}'); """.format(user_id, item_id)
    sqlite_api(db, sql, "write")

    flash("Item has been added to cart.", "success")
    return redirect(url_for("process_control.inventory_pc"))

#VIEW ITEM IMAGE#
@process_control.route('/pc/inventory/displayImage/<int:item_id>')
@login_required
def inventory_display_image(item_id):

    sql = """ SELECT image, itemName FROM Inventory WHERE id = {} """.format(item_id)
    items = sqlite_api(db, sql, "read")
    item = items[0]

    return "<img src='{}' />".format(url_for('static', filename= 'InventoryPics/'+ item['image']))

#ITEM DETAILS#
@process_control.route('/pc/inventory/details/<int:item_id>')
@login_required
def inventory_details(item_id):
    user_id = current_user.id

    cart = []
    sql = """ SELECT * FROM Cart WHERE userId = {} """.format(user_id)
    cart = sqlite_api(db, sql, "read")

    sql = """ SELECT * FROM Inventory WHERE id = {} """.format(item_id)
    items = sqlite_api(db, sql, "read")
    item = items[0]

    return render_template("process_control/inventory_details.html", item = item, cart = cart)

#JSON RETURN#
@process_control.route('/pc/inventory/json/<string:value>')
def inventory_json(value):
    results = []

    #get data from database#
    sql = """ SELECT * FROM Inventory """
    results = sqlite_api(db, sql, "read")
    
    return jsonify(results)

#DELETE ITEM#
@process_control.route('/pc/inventory/delete/<int:item_id>', methods=["GET","POST"])
@login_required
def inventory_pc_delete(item_id):

    sql = """ DELETE FROM Inventory WHERE id = '{}' """.format(item_id)
    sqlite_api(db, sql, "write")

    # Send log #
    now_log = datetime.now()
    send_log(f'{current_user.username}, deleted item: {item_id} at {now_log}', 'InventoryActivity')
        
    flash("Item has been deleted", "success")
    return redirect (url_for("process_control.inventory_pc"))

#ANSWER QUESTIONARE FOR LOCATION ID#
@process_control.route('/pc/inventory/questionare', methods=["GET", "POST"])
@login_required
def inventory_pc_questionare():
    form = InventoryQuestionareForm()
    system_choices = [(0,""), (1,"Optical Drives"), (2, "Internal Computer Components"),
                      (3, "Computer Accessories"), (4, "Optical Data Storage"),
                      (5, "Hard Drives"), (6, "Computer Expansion Cards"), (7, "Computer Power Supplies"),
                       (8, "Network Devices"), (9, "ABB/Bailey"),
                       (10, "HTRC"), (11, "Mouse"), (12, "Keyboard"), (13, "Software")]
    form.system.choices = system_choices
    
    if form.validate_on_submit():
        system = form.system.data
        manufacturer = form.manufacturer.data
        selected = system_choices[system][0]

        switcher = {
                1: "PC1-1",
                2: "PC1-2",
                3: "PC1-3",
                4: "PC1-4",
                5: "PC1-5",
                6: "PC1-6",
                7: "PC1-7",
                8: "PC1-8",
                9: "ABB",
                10: "HTRC",
                11: "PC2-1",
                12: "PC2-2",
                13: "SFT1"
            }

        if selected == 13:
            location_id = switcher[selected] + "-" + manufacturer[0].upper()
        else:
            location_id = switcher[selected]

        sql = """ SELECT locationId FROM Inventory WHERE locationId LIKE "{}%" """.format(location_id)
        location_ids = []
        locations = sqlite_api(db, sql, "read")
        if locations:
            locations = [location["locationId"] for location in locations]
            
            location_numbers = []
            for location in locations:
                location_number = location.split('-')[-1]
                location_numbers.append(int(location_number))

            location_numbers.sort()

            for i in range(len(location_numbers) -1):
                first = location_numbers[i]
                second = location_numbers[i + 1]
                if (first + 1) == second:
                    pass
                else:
                    new_number = str(first + 1)
        else:
            new_number = "1"
        location_id = location_id + "-" + new_number

        return redirect(url_for("process_control.inventory_pc_new", location_id = location_id, manufacturer=manufacturer))
    return render_template("process_control/inventory_questionare.html", form=form)

#UPDATE ITEM#
@process_control.route('/pc/inventory/update/<int:item_id>', methods=["GET","POST"])
@login_required
def inventory_pc_update(item_id):

    sql = """ SELECT * FROM Inventory WHERE id = '{}' """.format(item_id)
    items = sqlite_api(db, sql, "read")
    item = items[0]
    if item['image']:
        picture_file = item['image']
        oldPic = item['image']
    
    form = InventoryUpdateForm()
    
    # fill select field in with values #
    if request.method == "GET":
        form.item_name.data = item["itemName"]
        form.location_id.data = item["locationId"]
        form.quantity.data = item["quantity"]
        form.manufacturer.data = item["manufacturer"]
        form.model.data = item["model"]
        form.picture.data = item["image"]
        form.part_number.data = item["partNumber"]
        form.serial_number.data = item["serialNumber"]
        form.details.data = item["details"]
        form.category.data = item["category"]
        form.refItem.data = item["refItem"]
        form.vendor.data = item["vendor"]
        form.sap_id.data = item["SapId"]
        form.last_cost.data = item["LastCost"]
        
    if form.validate_on_submit():
        #get data from form #
        user = current_user.id
        item_name = form.item_name.data
        location_id = form.location_id.data
        quantity = form.quantity.data
        manufacturer = form.manufacturer.data
        model = form.model.data
        picture = form.picture.data
        part_number = form.part_number.data
        serial_number = form.serial_number.data
        details = form.details.data
        category = form.category.data
        refItem = form.refItem.data
        vendor = form.vendor.data
        sap_id = form.sap_id.data
        last_cost = form.last_cost.data
        
        #clean details data#
        details = details.replace('”', '"')
        details = details.replace('“', '"')
        details = details.replace("’", "'")
        details = details.replace("'", "''")

        #Resize and Save Picture#
        if picture:
            if oldPic != None:
                delete_picture(oldPic)
            picture_file = save_picture(picture)


        #Update Item in database#
        sql = """ UPDATE Inventory SET itemName = '{}',
locationId = '{}',
quantity = '{}',
manufacturer = '{}',
model = '{}',
image = '{}',
partNumber = '{}',
serialNumber = '{}',
details = '{}',
category = '{}',
refItem = '{}',
vendor = '{}',
SapId = '{}',
LastCost = '{}'WHERE id = '{}'""".format(item_name,location_id,
                                       quantity, manufacturer,
                                       model, picture_file,
                                       part_number, serial_number,
                                       details, category,
                                       refItem, vendor,
                                       sap_id, last_cost,
                                        item_id)
        sqlite_api(db, sql, "write")
        

        #send log#
        now_log = datetime.now()
        send_log(f'{current_user.username}, updated item: {item_name} at {now_log}', 'InventoryActivity')
        
        #Redirect to inventory page.#
        flash("Item has been updated", "success")
        return redirect (url_for("process_control.inventory_pc"))
    return render_template("process_control/inventory_new.html", form = form, title = "Update Item", legend = "Update Item")

#CREATE ITEM#
@process_control.route('/pc/inventory/new/<location_id>/<manufacturer>', methods=["GET","POST"])
@login_required
def inventory_pc_new(location_id, manufacturer):
    form = InventoryForm()

    form.location_id.data = location_id
    form.manufacturer.data = manufacturer
    # fill select field in with values #
    if request.method == "GET":
        pass
    if form.validate_on_submit():
        #get data from form #
        user = current_user.id
        item_name = form.item_name.data
        location_id = form.location_id.data
        quantity = form.quantity.data
        manufacturer = form.manufacturer.data
        model = form.model.data
        picture = form.picture.data
        part_number = form.part_number.data
        serial_number = form.serial_number.data
        details = form.details.data
        category = form.category.data
        refItem = form.refItem.data
        vendor = form.vendor.data
        sap_id = form.sap_id.data
        last_cost = form.last_cost.data
        
        #clean details data#
        details = details.replace('”', '"')
        details = details.replace('“', '"')
        details = details.replace("’", "'")
        details = details.replace("'", "''")

        #Resize and Save Picture#
        if picture:
            picture_file = save_picture(picture)
        else:
            picture_file = "default.jpg"

        #Submit to database#
        sql = """ INSERT INTO Inventory (itemName, locationId, quantity, manufacturer,
            model, image, partNumber, serialNumber,details, category, refItem, vendor, SapId, LastCost)
            VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'); """.format(item_name,
                                                                                                 location_id,
                                                                                                 quantity,
                                                                                                 manufacturer,
                                                                                                 model,
                                                                                                 picture_file,
                                                                                                 part_number,
                                                                                                 serial_number,
                                                                                                 details,
                                                                                                 category,
                                                                                                 refItem,
                                                                                                 vendor,
                                                                                                 sap_id,
                                                                                                last_cost)
        sqlite_api(db, sql, 'write')

            #Send Log#
        now_log = datetime.now()
        send_log(f'{current_user.username}, created item: {item_name} at {now_log}', 'InventoryActivity')

        flash("Item has been created", "success")
        return redirect (url_for("process_control.inventory_pc"))

    return render_template('process_control/inventory_new.html', form=form, title="New Item", legend="Create Item")

