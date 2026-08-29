from flask import Blueprint, render_template
from app.models import Warranty
warranties_bp=Blueprint('warranties',__name__)
@warranties_bp.route('/')
def list_warranties(): return render_template('warranty.html',warranties=Warranty.query.all())
