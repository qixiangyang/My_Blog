"""
Description:
Author:qxy
Date: 2019/10/24 3:34 下午
File: views 
"""

from flask import render_template, redirect, request, url_for, flash, session, current_app
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.filter(User.email == email).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next_url = request.args.get('next')
            session.permanent = True
            if next_url is None or not next_url.startswith('/'):
                next_url = url_for('blog.contents')
            return redirect(next_url)

        if user is None:
            current_app.logger.info(f"email_not_found => email: {email}")

        if user and user.verify_password(form.password.data) is False:
            current_app.logger.info(f"password_error")

        flash('email or email error.', category="danger")
        return redirect(url_for('auth.login'))

    if form.validate() is False:
        flash('Input data format error', category="danger")

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category="info")
    return redirect(url_for('auth.login'))