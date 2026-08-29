from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import MaintenanceRequest
maintenance_bp=Blueprint('maintenance',__name__)
@maintenance_bp.route('/', methods=['GET','POST'])
def maintenance():
    if request.method=='POST':
        r=MaintenanceRequest(customer_name=request.form.get('customer_name','Customer'),service_type=request.form['issue_type'],issue_description=request.form['description']); db.session.add(r); db.session.commit(); flash('Maintenance request submitted.','success'); return redirect(url_for('maintenance.maintenance'))
    return render_template('maintenance.html',maintenance_requests=MaintenanceRequest.query.order_by(MaintenanceRequest.id.desc()).all())
@maintenance_bp.route('/list')
def list_requests(): return maintenance()
