from flask import render_template, url_for, flash, redirect, request, Blueprint


dev_ops = Blueprint('dev_ops', __name__)

@dev_ops.route('/api')
def api():
    return render_template('api.html')

@dev_ops.route('/api/new')
def api_new():
    return render_template('api_new.html')

