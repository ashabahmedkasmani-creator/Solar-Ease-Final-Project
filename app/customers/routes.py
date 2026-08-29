from flask import Blueprint, render_template, session, redirect, url_for
from app.models import Requirement, Survey, Quotation, Installation
customers_bp=Blueprint('customers',__name__)
@customers_bp.route('/dashboard')
def dashboard():
    uid=session.get('user_id')
    if not uid: return redirect(url_for('auth.login'))
    latest_req=Requirement.query.filter_by(user_id=uid).order_by(Requirement.id.desc()).first()
    latest_survey=Survey.query.filter_by(user_id=uid).order_by(Survey.id.desc()).first()
    quotations=Quotation.query.order_by(Quotation.id.desc()).all()
    projects=Installation.query.order_by(Installation.id.desc()).all()
    return render_template('user_dashboard.html',latest_req=latest_req,latest_survey=latest_survey,quotations=quotations,projects=projects)
