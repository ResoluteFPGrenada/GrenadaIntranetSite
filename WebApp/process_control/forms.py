from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, IntegerField, SubmitField, SelectField, TextAreaField, DecimalField)
from wtforms.validators import DataRequired, Length, ValidationError
from WebApp.api.sqlite_tool import sqlite_api

db = "./app/WebApp/databases/inventory.db"

class InventoryQuestionareForm(FlaskForm):
    system = SelectField("What Best Describes Your Item?",
                         coerce=int,
                         validators=[DataRequired()])

    manufacturer = StringField("Manufacturer.",
                               validators=[DataRequired()])

    submit = SubmitField("Continue")

class InventoryUpdateForm(FlaskForm):
    item_name = StringField("Item Name",
                            validators=[DataRequired()])

    location_id = StringField("Locatino Id",
                              validators=[DataRequired()])

    quantity = IntegerField("Quantity",
                            validators=[DataRequired()])

    manufacturer = StringField("Manufacturer")

    model = StringField("Model")

    picture = FileField("Picture", validators=[FileAllowed(['jpg', 'png'])])

    part_number = StringField("Part Number")

    serial_number = StringField("Serial Number")

    details = TextAreaField("Details",
                            validators=[DataRequired()])

    category = StringField("Category",
                           validators=[DataRequired()])

    refItem = StringField("Reference Item",
                        validators=[DataRequired()])

    vendor = StringField("Vendor")

    sap_id = StringField(" SAP ID ")

    last_cost = DecimalField("Last Purchase Cost (dollar per unit)",
                             validators=[DataRequired()])

    submit = SubmitField(" Update Item ")

class InventoryForm(FlaskForm):
    item_name = StringField("Item Name",
                            validators=[DataRequired()])

    location_id = StringField("Locatino Id",
                              validators=[DataRequired()])

    quantity = IntegerField("Quantity",
                            validators=[DataRequired()])

    manufacturer = StringField("Manufacturer")

    model = StringField("Model")

    picture = FileField("Picture", validators=[FileAllowed(['jpg', 'png'])])

    part_number = StringField("Part Number")

    serial_number = StringField("Serial Number")

    details = TextAreaField("Details",
                            validators=[DataRequired()])

    category = StringField("Category",
                           validators=[DataRequired()])

    refItem = StringField("Reference Item",
                        validators=[DataRequired()])

    vendor = StringField("Vendor")

    sap_id = StringField(" SAP ID ")

    last_cost = DecimalField("Last Purchase Cost (dollar per unit)",
                             validators=[DataRequired()])

    submit = SubmitField(" Create Item ")

    def validate_location_id(self, location_id):
        sql = """ SELECT * FROM Inventory WHERE locationId = '{}' """.format(location_id.data)
        locationIds = sqlite_api(db, sql, "read")
        if locationIds:
            raise ValidationError("That Location is taken, Please contact administrator to fix this problem")

    def validate_part_number(self, part_number):
        sql = """ SELECT * FROM Inventory WHERE partNumber = '{}' """.format(part_number.data)
        partNumber = sqlite_api(db, sql, "read")
        if partNumber:
            raise ValidationError("An item with this part number already exists, please search inventory for this item.")

    def validate_serial_number(self, serial_number):
        sql = """ SELECT * FROM Inventory WHERE serialNumber = '{}' """.format(serial_number.data)
        serialNumber = sqlite_api(db, sql, "read")
        if serialNumber:
            raise ValidationError("An item with this serial number already exists, please search inventory for this item.")

    def validate_sap_id(self, sap_id):
        sql = """ SELECT * FROM Inventory WHERE SapId = '{}' """.format(sap_id.data)
        sapId = sqlite_api(db, sql, "read")
        if sapId:
            raise ValidationError("An item with this SAP Id already exists, please search inventory for this item.")
