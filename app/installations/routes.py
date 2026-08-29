from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Installation, Quotation, Warranty
from app.auth.decorators import login_required, role_required
installations_bp=Blueprint('installations',__name__)
@installations_bp.route('/')
@login_required
def list_installations(): return render_template('installation_tracking.html',projects=Installation.query.order_by(Installation.id.desc()).all())
@installations_bp.route('/schedule/<int:quote_id>', methods=['GET','POST'])
@role_required('admin')
def schedule(quote_id):
    q=Quotation.query.get_or_404(quote_id)
    if request.method=='POST':
        inst=Installation(quotation_id=q.id,team_lead=request.form.get('team_lead','Not Assigned'),technician=request.form.get('technician','Not Assigned'),capacity_kw=q.system_capacity_kw,address=request.form.get('address',''),status='Scheduled'); db.session.add(inst); db.session.commit(); flash('Installation scheduled!','success'); return redirect(url_for('installations.list_installations'))
    return render_template('installation_tracking.html',projects=[q.installation] if q.installation else [])
@installations_bp.route('/update/<int:installation_id>', methods=['POST'])
@role_required('admin')
def update(installation_id):
    i=Installation.query.get_or_404(installation_id); i.status=request.form.get('status',i.status); i.technician=request.form.get('technician',i.technician)
    if i.status == 'Completed & Handover' and not Warranty.query.first():
        db.session.add(Warranty(component_name='Solar Installation System', serial_number=f'SE-PRJ-{i.id:05d}', warranty_years=10, start_date=__import__('datetime').date.today().isoformat()))
    db.session.commit(); flash('Installation progress updated.','success'); return redirect(url_for('installations.list_installations'))
