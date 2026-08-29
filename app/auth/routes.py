from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User
from app.roles import dashboard_for, label_for
from app.utils import unique_username
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email','').strip().lower(); password=request.form.get('password','')
        user=User.query.filter_by(email=email).first()
        valid=user and (check_password_hash(user.password,password) if user.password.startswith(('scrypt:','pbkdf2:','argon2:')) else user.password==password)
        if not valid:
            flash('Invalid email or password.', 'danger'); return redirect(url_for('auth.login'))
        session['user_id']=user.id; session['user_name']=user.full_name; session['role']=user.role
        flash(f'Welcome back, {user.full_name} ({label_for(user.role)}).', 'success')
        return redirect(url_for(dashboard_for(user.role)))
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        full_name=request.form.get('full_name','').strip(); email=request.form.get('email','').strip().lower(); password=request.form.get('password','')
        if not full_name or not email or not password:
            flash('Please fill in your name, email and password.', 'warning'); return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in instead.', 'warning'); return redirect(url_for('auth.register'))
        try:
            user=User(full_name=full_name, username=unique_username(email.split('@')[0]), email=email, password=generate_password_hash(password), role='customer')
            db.session.add(user); db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Something went wrong while creating your account. Please try again.', 'danger')
            return redirect(url_for('auth.register'))
        flash('Registration successful. Please log in.', 'success'); return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear(); flash('You have been logged out.', 'info'); return redirect(url_for('index'))
