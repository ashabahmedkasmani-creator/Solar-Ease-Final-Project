from flask import Blueprint, render_template
from app.models import Warranty
from app.auth.decorators import login_required
warranties_bp=Blueprint('warranties',__name__)
@warranties_bp.route('/')
@login_required
def list_warranties(): return render_template('warranty.html',warranties=Warranty.query.all())
