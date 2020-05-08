from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint,
                   jsonify, abort)
from operator import attrgetter
from flask_login import login_user, current_user, logout_user, login_required
from WebApp import db, bcrypt
from WebApp.models import User, Link, Role
from WebApp.admin.forms import (RegistrationForm, RoleForm,
                                PermissionForm, RoleModForm,
                                NewLinkForm, UpdateLinkForm)
from WebApp.admin.utils import available_roles, available_rights

admin = Blueprint('admin', __name__)


@admin.route('/links/new', methods=('GET','POST'))
def new_links():
    form = NewLinkForm()
    if form.validate_on_submit():
        link = Link(linkname=form.linkname.data, url=form.url.data, group=form.group.data)
        db.session.add(link)
        db.session.commit()
        flash('link has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('admin/new_links.html', legend='Create Link', title='New Links', form=form)

@admin.route('/links/<int:link_id>/update', methods=('GET','POST'))
@login_required
def update_links(link_id):
    link = Link.query.get_or_404(link_id)
    if not current_user.is_admin:
        abort(403)

    form = UpdateLinkForm()
    if request.method == 'GET':
        form.linkname.data = link.linkname
        form.url.data = link.url
        form.group.data = link.group
    elif form.validate_on_submit():
        link.linkname = form.linkname.data
        link.url = form.url.data
        link.group = form.group.data
        db.session.commit()
        flash('Link has been updated', 'success')
        return redirect(url_for('main.home'))
    return render_template('admin/update_links.html', title='New Link', legend='Update Link', form=form)

@admin.route('/links/<int:link_id>/delete', methods=('GET','POST'))
@login_required
def delete_links(link_id):
    link = Link.query.get_or_404(link_id)
    if not current_user.is_admin:
        abort(403)
    db.session.delete(link)
    db.session.commit()
    
    flash('Link was delete from database', 'success')
    return redirect(url_for('main.home'))


    
@admin.route('/permissions', methods=('GET', 'POST'))
def permissions():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    elif not current_user.is_admin:
        return redirect(url_for('main.home'))
    form = PermissionForm()
    if request.method == 'GET':
        users = User.query.all()
        users.sort(key=attrgetter('username'))
        form.username.choices = [(int(user.id), user.username) for user in users]   
        user = users[0]
        roles = Role.query.all()
        rights = user.rights
        availables = available_roles(roles, user)
        form.roles.choices = [(int(available.id), available.group) for available in availables]
        form.assigned.choices = [(int(right.id), right.group) for right in user.rights]
    elif request.method == 'POST':
        form_username = []
        form_roles = []
        form_assigned = []
        form_username = form.username.data
        form_roles = form.roles.data
        form_assigned = form.assigned.data
        user = User.query.filter_by(id=form_username).first()
        if form_roles is not None:
            role_ids = form_roles
            roles = [Role.query.filter_by(id=role_id).first() for role_id in role_ids] 
            availables = available_rights(roles, user)
            if isinstance(availables, list):
                for available in availables:
                    try:
                        user.rights.remove(available)
                    except:
                        pass
            else:
                    try:
                        user.rights.remove(availables)
                    except:
                        pass
            
        if form_assigned is not None:
            assigned_ids = form_assigned
            assigned = [Role.query.filter_by(id=assigned_id).first() for assigned_id in assigned_ids]
            assignables = available_roles(assigned, user)
            if isinstance(assignables, list):
                for assignable in assignables:
                        try:
                            user.rights.append(assignable)
                        except:
                            pass
            else:
                    try:
                        user.rights.append(assignables)
                    except:
                        pass
            flash('Permissions for {} have been updated.'.format(user.username), 'success')
        db.session.commit()
        return redirect(url_for('admin.permissions'))
    
    return render_template('admin/permissions.html', title='Permissions', form=form)

@admin.route('/permissions_user/<username_id>')
def permissions_user(username_id):
    user = User.query.filter_by(id=username_id).first()
    rights = user.rights
    roles = Role.query.all()
    availables = available_roles(roles, user)
    
        # create export objects
    rights_objs = []
    availables_objs = []
    for right in rights:
        obj = {}
        obj['id'] = '{}'.format(right.id)
        obj['group'] = '{}'.format(right.group)
        rights_objs.append(obj)

    for available in availables:
        obj = {}
        obj['id'] = '{}'.format(available.id)
        obj['group'] = '{}'.format(available.group)
        availables_objs.append(obj)
        
    return jsonify(rights_objs, availables_objs)

@admin.route('/new_roles', methods=('GET', 'POST'))
def new_roles():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    elif not current_user.is_admin:
        return redirect(url_for('main.home'))
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(group=form.group.data, description=form.description.data)
        db.session.add(role)
        db.session.commit()
        flash('A new role as been created.', 'success')
        return redirect(url_for('admin.permissions'))
    return render_template('admin/new_roles.html', title='New Roles', form=form)

@admin.route('/roles', methods=('GET', 'POST'))
def roles():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    elif not current_user.is_admin:
        return redirect(url_for('main.home'))
    form = RoleModForm()
    if request.method == "POST":
        role = []
        role = Role.query.filter_by(id=form.group.data).first()
        role.description = form.description.data
        db.session.commit()
        flash('a role has been updated ', 'success')
        return redirect(url_for('main.home'))
    elif request.method == "GET":
        form.group.choices = [(role.id, role.group) for role in Role.query.all()]
        role = Role.query.filter_by(id=1).first()
        form.description.data = role.description
        
    return render_template('admin/roles.html', title='Update Roles',form=form)

@admin.route('/roles_group/<group_id>')
def roles_group(group_id):
    role = Role.query.filter_by(id=group_id).first()
    obj = {}
    obj['id'] = '{}'.format(role.id)
    obj['group'] = '{}'.format(role.group)
    obj['description'] = '{}'.format(role.description)
    
    return jsonify(obj)

@admin.route('/register', methods=['GET','POST'])
def register():
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))
    elif not current_user.is_admin:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, is_admin=form.admin.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are able to log in.!', 'success')
        return redirect(url_for('users.login'))
    return render_template('admin/register.html', title='Register',form=form)

@admin.route('/admin/reset_password/<int:user_id>')
def password_reset(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))
    elif not current_user.is_admin:
        return redirect(url_for('main.home'))

    pword = "Passw0rd"

    hashed_password = bcrypt.generate_password_hash(pword).decode('utf-8')
    user = User.query.filter_by(id=user_id).first()
    user.password = hashed_password
    db.session.commit()
    flash('Password has been reset to {}'.format(pword), 'success')
    return redirect(url_for('main.home'))

@admin.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    elif not current_user.is_admin:
        return redirect(url_for('main.home'))

    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('{} has been deleted!'.format(user.username), 'success')
    return redirect(url_for('main.home'))
    
