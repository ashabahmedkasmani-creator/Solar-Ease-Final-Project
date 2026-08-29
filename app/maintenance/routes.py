from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import MaintenanceRequest
from app.auth.decorators import login_required, role_required

maintenance_bp=Blueprint('maintenance',__name__)

@maintenance_bp.route('/', methods=['GET','POST'])
@login_required
def maintenance():
    if request.method=='POST':
        r=MaintenanceRequest(customer_name=request.form.get('customer_name','Customer'),service_type=request.form['issue_type'],issue_description=request.form['description']); db.session.add(r); db.session.commit(); flash('Maintenance request submitted.','success'); return redirect(url_for('maintenance.maintenance'))
    return render_template('maintenance.html',maintenance_requests=MaintenanceRequest.query.order_by(MaintenanceRequest.id.desc()).all())

@maintenance_bp.route('/list')
@login_required
def list_requests(): return maintenance()

@maintenance_bp.route('/update/<int:request_id>', methods=['POST'])
@role_required('admin','technician','engineer')
def update_status(request_id):
    r = MaintenanceRequest.query.get_or_404(request_id)
    r.status = request.form.get('status', r.status)
    db.session.commit()
    flash('Maintenance request status updated.', 'success')
    return redirect(url_for('maintenance.maintenance'))
