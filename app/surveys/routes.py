from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Survey
from app.auth.decorators import login_required, role_required
surveys_bp=Blueprint('surveys',__name__)
@surveys_bp.route('/', methods=['GET','POST'])
@login_required
def index():
    if request.method=='POST':
        s=Survey(user_id=session.get('user_id'),customer_name=session.get('user_name','Customer'),phone=request.form.get('phone',''),city=request.form.get('city','Karachi'),address=request.form['address'],preferred_date=request.form['preferred_date'],preferred_time=request.form['preferred_time'],property_type=request.form.get('property_type','Residential'),contact_person=request.form.get('contact_person',''),notes=request.form.get('notes',''),status='Requested')
        db.session.add(s); db.session.commit(); flash('Site survey request submitted successfully!','success'); return redirect(url_for('surveys.index'))
    return render_template('survey_booking.html')
@surveys_bp.route('/list')
def list_surveys(): return render_template('survey_booking.html')
@surveys_bp.route('/new', methods=['GET','POST'])
def new_survey(): return index()
@surveys_bp.route('/admin/update/<int:survey_id>', methods=['POST'])
@role_required('admin')
def update_survey(survey_id):
    s=Survey.query.get_or_404(survey_id); s.engineer=request.form.get('engineer',s.engineer); s.status=request.form.get('status',s.status); s.report_notes=request.form.get('report_notes',s.report_notes); s.roof_area=float(request.form.get('roof_area',s.roof_area) or 0); s.recommended_kw=float(request.form.get('recommended_kw',s.recommended_kw) or 0); db.session.commit(); flash('Survey report updated.','success'); return redirect(url_for('admin.dashboard'))
