from flask import render_template, request, Blueprint
from WebApp.models import Link
from WebApp.main.forms import DataSetForm
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
@main.route('/grenada')
def home():
    links = Link.query.all()
    groups = []
    for link in links:
        if not link.group in groups:
            groups.append(link.group)
            
    return render_template('home.html', groups=groups, links=links)

@main.route('/dashboard/')
@login_required
def dashboard():
    username = current_user.username
    user_id = current_user.id
    return render_template('dashboard.html', title=f"{username}'s Dashboard")

@main.route('/dashboard/widget/')
@login_required
def widgets():
    username = current_user.username
    user_id = current_user.id
    return render_template('widgets.html', title=f"{username}'s Widgets")

@main.route('/dashboard/dataset/')
@login_required
def dataSets():
    username = current_user.username
    user_id = current_user.id
    return render_template('dataSets.html', title=f"{username}'s Datasets")

@main.route('/dashboard/dataset/new')
@login_required
def dataSet_new():
    form = DataSetForm
    return render_template('dataSet_new.html', title='New Dataset', legend='Create Dataset', form=form)
