from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Payment, Quotation, Installation, Warranty
from app.auth.decorators import login_required, role_required

payments_bp=Blueprint('payments',__name__)

@payments_bp.route('/', methods=['GET','POST'])
@payments_bp.route('/history', methods=['GET','POST'])
@login_required
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
@login_required
def process_payment(project_id):
    q=Quotation.query.get_or_404(project_id); request.form.get('payment_method'); return history()

@payments_bp.route('/finance')
@role_required('finance')
def finance_dashboard():
    payments = Payment.query.order_by(Payment.id.desc()).all()
    pending_verification = [p for p in payments if p.status == 'Payment Verification Required']
    verified = [p for p in payments if p.status != 'Payment Verification Required']
    total_revenue = sum(p.amount_paid for p in payments if p.status != 'Failed')
    outstanding = sum(q.final_amount - sum(pp.amount_paid for pp in q.payments) for q in Quotation.query.filter_by(status='Approved').all())
    return render_template('finance_dashboard.html', pending_verification=pending_verification, verified=verified,
        total_revenue=total_revenue, outstanding=outstanding, payments=payments)

@payments_bp.route('/verify/<int:payment_id>', methods=['POST'])
@role_required('finance')
def verify_payment(payment_id):
    p = Payment.query.get_or_404(payment_id)
    action = request.form.get('action', 'verify')
    q = p.quotation
    if action == 'reject':
        p.status = 'Failed'
        flash('Payment marked as failed.', 'warning')
    else:
        paid_so_far = sum(pp.amount_paid for pp in q.payments if pp.status != 'Failed')
        p.status = 'Fully Paid' if paid_so_far >= q.final_amount else 'Partially Paid'
        q.status = 'Fully Paid' if paid_so_far >= q.final_amount else 'Partially Paid'
        flash(f'Payment verified for {q.quotation_number}.', 'success')
    db.session.commit()
    return redirect(url_for('payments.finance_dashboard'))
