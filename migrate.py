from WebApp import create_app, db, bcrypt
from WebApp.models import User, Link, Role, access
import json

db.create_all(app=create_app())
app = create_app()

# import JSON file  #
with open('site.json', 'r') as json_file:
        json_data = json_file.read()
        print(json_data)
        data = json.loads(json_data)
        #print(data)
        #for d in data['link1']:
        #    print(d.group)

# parse JSON file #

# Sort Json content into table groups #

# remove table attribute from each object #

ctx = app.app_context()
ctx.push()

# for loop through each table group #
# for each object in group create based on that table's lable#

#in try except block#

ctx.pop()
exit()


