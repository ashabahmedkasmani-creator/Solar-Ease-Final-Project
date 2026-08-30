from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User, Survey, Quotation, Installation, Inventory, MaintenanceRequest, Role, Permission
# from app.models.models import User, Role, Permission  # Import update kar lein
from app.auth.decorators import role_required
from app.roles import ROLES, STAFF_ROLES, label_for
from app.utils import unique_username
from werkzeug.security import generate_password_hash

sajid_bp=Blueprint('sajid',__name__)

@sajid_bp.route('/sajju')
@role_required('admin')
def dashboard():
    # return render_template('admin_dashboard.html',
    #     total_users=User.query.count(), total_surveys=Survey.query.count(),
    #     total_quotations=Quotation.query.count(), total_projects=Installation.query.count(),
    #     surveys=Survey.query.order_by(Survey.id.desc()).all(), inventory=Inventory.query.all(),
    #     complaints_open=MaintenanceRequest.query.filter(MaintenanceRequest.status!='Resolved').count())
    return render_template('sajju.html',
        total_users=User.query.count(), total_surveys=Survey.query.count(),
        total_quotations=Quotation.query.count(), total_projects=Installation.query.count(),
        surveys=Survey.query.order_by(Survey.id.desc()).all(), inventory=Inventory.query.all(),
        complaints_open=MaintenanceRequest.query.filter(MaintenanceRequest.status!='Resolved').count())

@sajid_bp.route('/users')
@role_required('admin')
def users():
    return render_template('sajid_users.html', users=User.query.order_by(User.id.desc()).all(),
        roles=ROLES, staff_roles=STAFF_ROLES, label_for=label_for)

# @sajid_bp.route('/permissions')
# @role_required('admin')
# # def permissions():
# #     return render_template('sajid_permissions.html', users=User.query.order_by(User.id.desc()).all(),
# #         roles=ROLES, staff_roles=STAFF_ROLES, label_for=label_for)
# def permissions():
#     # Database se saari dynamic Roles aur Permissions fetch karein
#     db_roles = Role.query.all()
#     db_permissions = Permission.query.all()
#     users = User.query.order_by(User.id.desc()).all()

#     return render_template(
#         'sajid_permissions.html', 
#         users=users,
#         roles=ROLES,                 # Aapka purana dict/list backup ke liye
#         staff_roles=STAFF_ROLES,     # Aapka purana staff roles list
#         label_for=label_for,
#         db_roles=db_roles,           # Naya dynamic roles data
#         db_permissions=db_permissions # Saare permissions (Checkboxes banane ke liye)
#     )






# 1. Main Permissions Page: Yahan sirf Roles ki List dikhegi (Cards / Table form me)
@sajid_bp.route('/roles')
@role_required('admin')
def roles():
    db_roles = Role.query.all()
    return render_template('sajid_roles_list.html', roles=db_roles)

# 2. Specific Role edit page: e.g. /permissions/role/2 (Edit permissions for Sales)
@sajid_bp.route('/permissions/role/<int:role_id>', methods=['GET', 'POST'])
@role_required('admin')
def edit_role_permissions(role_id):
    role = Role.query.get_or_404(role_id)
    
    if request.method == 'POST':
        selected_perm_ids = request.form.getlist('permissions')
        selected_perms = Permission.query.filter(Permission.id.in_(selected_perm_ids)).all()
        role.permissions = selected_perms
        db.session.commit()
        
        flash(f'{role.label} ke permissions successfully update ho gaye!', 'success')
        return redirect(url_for('sajid.permissions'))

    all_permissions = Permission.query.order_by(Permission.category).all()
    
    # Permissions ko category ke hisab se group kar rahe hain taake UI par clean dikhe
    permissions_by_category = {}
    for perm in all_permissions:
        cat = perm.category or 'General'
        if cat not in permissions_by_category:
            permissions_by_category[cat] = []
        permissions_by_category[cat].append(perm)

    return render_template(
        'sajid_permissions_edit.html', 
        role=role, 
        permissions_by_category=permissions_by_category
    )




@sajid_bp.route('/users/create', methods=['POST'])
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

# @admin_bp.route('/users/role/<int:user_id>', methods=['POST'])
# @role_required('admin')
# def update_role(user_id):
#     user = User.query.get_or_404(user_id)
#     new_role = request.form.get('role')
#     if new_role in ROLES:
#         user.role = new_role
#         db.session.commit()
#         flash(f"{user.full_name}'s role updated to {label_for(new_role)}.", 'success')
#     return redirect(url_for('admin.users'))
