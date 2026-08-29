from flask import Blueprint, render_template
from app.models import User, Survey, Quotation, Installation, Inventory
admin_bp=Blueprint('admin',__name__)
@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin_dashboard.html',total_users=User.query.count(),total_surveys=Survey.query.count(),total_quotations=Quotation.query.count(),total_projects=Installation.query.count(),surveys=Survey.query.order_by(Survey.id.desc()).all(),inventory=Inventory.query.all())
