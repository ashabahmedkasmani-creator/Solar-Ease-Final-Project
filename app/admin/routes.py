from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User, Survey, Quotation, Installation, Inventory, MaintenanceRequest
from app.auth.decorators import role_required
from app.roles import ROLES, STAFF_ROLES, label_for
from app.utils import unique_username
from werkzeug.security import generate_password_hash

admin_bp=Blueprint('admin',__name__)

@admin_bp.route('/dashboard')
@role_required('admin')
def dashboard():
    return render_template('admin_dashboard.html',
        total_users=User.query.count(), total_surveys=Survey.query.count(),
        total_quotations=Quotation.query.count(), total_projects=Installation.query.count(),
        surveys=Survey.query.order_by(Survey.id.desc()).all(), inventory=Inventory.query.all(),
        complaints_open=MaintenanceRequest.query.filter(MaintenanceRequest.status!='Resolved').count())

@admin_bp.route('/users')
@role_required('admin')
def users():
    return render_template('admin_users.html', users=User.query.order_by(User.id.desc()).all(),
        roles=ROLES, staff_roles=STAFF_ROLES, label_for=label_for)

@admin_bp.route('/users/create', methods=['POST'])
@role_required('admin')
def create_user():
    full_name = request.form.get('full_name','').strip()
    email = request.form.get('email','').strip().lower()
    role = request.form.get('role','sales')
    password = request.form.get('password','changeme123')
    if role not in STAFF_ROLES:
        flash('Invalid staff role selected.', 'danger'); return redirect(url_for('admin.users'))
    if User.query.filter_by(email=email).first():
        flash('A user with that email already exists.', 'warning'); return redirect(url_for('admin.users'))
    try:
        user = User(full_name=full_name, username=unique_username(email.split('@')[0]), email=email,
                    password=generate_password_hash(password), role=role)
        db.session.add(user); db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Something went wrong while creating that account. Please try again.', 'danger')
        return redirect(url_for('admin.users'))
    flash(f'{label_for(role)} account created for {full_name}.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/role/<int:user_id>', methods=['POST'])
@role_required('admin')
def update_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    if new_role in ROLES:
        user.role = new_role
        db.session.commit()
        flash(f"{user.full_name}'s role updated to {label_for(new_role)}.", 'success')
    return redirect(url_for('admin.users'))
