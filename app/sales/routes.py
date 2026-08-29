from flask import Blueprint, render_template
from app.models import SolarPackage
sales_bp=Blueprint('sales',__name__)
@sales_bp.route('/packages')
def packages(): return render_template('packages.html', packages=SolarPackage.query.all())
@sales_bp.route('/system-types')
def system_types():
    systems=[
        {'name':'On-Grid','description':'Connected to the electricity grid, normally without batteries. Suitable for bill reduction and net-metering documentation.','battery':'No','grid':'Yes','backup':'No'},
        {'name':'Off-Grid','description':'Independent from the electricity grid and designed around battery storage for remote locations.','battery':'Yes','grid':'No','backup':'Yes'},
        {'name':'Hybrid','description':'Grid-connected system with batteries that provides backup during outages.','battery':'Yes','grid':'Yes','backup':'Yes'},
    ]
    return render_template('system_types.html',systems=systems)
