# services/web/project/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.home'))

        flash('Invalid username or password', 'error')
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Log the user out by clearing the session."""
    session.clear()
    return redirect(url_for('main.home'))


@auth_bp.route('/create_account', methods=['GET', 'POST'])
def create_account():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm  = request.form['confirm']

        # Check password match
        if password != confirm:
            flash('Passwords must match', 'error')
            return render_template('create_account.html')

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return render_template('create_account.html')

        # Create and store the new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Auto-login the new user
        session.clear()
        session['user_id'] = new_user.id
        return redirect(url_for('main.home'))

    return render_template('create_account.html')

