from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Payment, Quotation, Installation, Warranty
payments_bp=Blueprint('payments',__name__)
@payments_bp.route('/', methods=['GET','POST'])
@payments_bp.route('/history', methods=['GET','POST'])
def history():
    if request.method=='POST':
        qid=int(request.form.get('quotation_id',0)); q=Quotation.query.get_or_404(qid); amount=q.final_amount*(0.30 if '30%' in request.form.get('payment_type','') else 1.0)
        p=Payment(quotation_id=q.id,payment_method=request.form['payment_method'],payment_type=request.form['payment_type'],trx_ref=request.form['trx_ref'],amount_paid=amount)
        db.session.add(p); q.status='Payment Verification Required'
        if not q.installation:
            db.session.add(Installation(quotation_id=q.id, capacity_kw=q.system_capacity_kw, status='Project Created'))
        db.session.commit(); flash('Payment record submitted for verification and installation project created.','success')
    payments=Payment.query.order_by(Payment.id.desc()).all(); approved=Quotation.query.filter(Quotation.status.in_(['Approved','Payment Verification Required','Partially Paid','Fully Paid'])).all(); project=approved[0] if approved else (Quotation.query.order_by(Quotation.id.desc()).first())
    return render_template('payment.html',payments=payments,project=project,quotations=approved)
@payments_bp.route('/process/<int:project_id>', methods=['POST'])
def process_payment(project_id):
    q=Quotation.query.get_or_404(project_id); request.form.get('payment_method'); return history()
