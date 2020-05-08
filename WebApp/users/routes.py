from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from WebApp import db, bcrypt
from WebApp.models import User, Link, access, Role
from WebApp.users.forms import (LoginForm, UpdateAccountForm,
                                RequestResetForm, ResetPasswordForm,
                                RegistrationRequestForm)
from WebApp.users.utils import save_picture, send_reset_email, send_email, send_log
import datetime

users= Blueprint('users', __name__)


@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            now_log = datetime.datetime.now()
            send_log(f'{current_user.username}, logged in, {now_log}', 'authentication')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('user/login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    now_log = datetime.datetime.now()
    send_log(f'{current_user.username}, logged out, {now_log}', 'authentication')

    logout_user()
    return redirect(url_for('main.home'))

@users.route('/request_register', methods=['GET', 'POST'])
def register():
    form = RegistrationRequestForm()
    if form.validate_on_submit():
        admins = User.query.filter_by(is_admin=True)
        receiver = [admin.email for admin in admins]
        #receiver = '{}'.format([admin.email for admin in admins])
        message = """MIME-Version: 1.0
Content-type: text/html
Subject: Grenada Intranet Request User Registry
Someone is requesting registration to the Grenada Intranet Site their email is {}""".format(form.email.data)
        #send_email(receiver, message)
        return f"{receiver}"
        
        #flash('Your request for access will be processed. Please watch your email for updates', 'success')
        #return redirect(url_for('main.home'))
    return render_template('user/registration.html', form=form)


@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='ProfilePics/' + current_user.image_file)
    return render_template('user/account.html', title='Account', image_file=image_file, form=form)


@users.route('/reset_password', methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('user/reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been changed. You are able to log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/reset_token.html', title='Reset Password', form=form)


