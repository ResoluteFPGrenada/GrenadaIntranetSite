from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required

rest_api = Blueprint('rest_api', __name__)

@rest_api.route('/NSC/create/<string:data>')
def nsc_new(data):
    return f"{data}"


