from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Inventory
inventory_bp=Blueprint('inventory',__name__)
@inventory_bp.route('/')
def stock(): return render_template('inventory_list.html',items=Inventory.query.all())
@inventory_bp.route('/add', methods=['GET','POST'])
def add_item():
    if request.method=='POST':
        item=Inventory(item_name=request.form['item_name'],category=request.form['category'],brand=request.form.get('brand','Generic'),model=request.form.get('model',''),quantity=int(request.form['quantity']),selling_price=float(request.form.get('selling_price',0) or 0),purchase_price=float(request.form.get('purchase_price',0) or 0),supplier=request.form.get('supplier','Local Supplier'),minimum_stock=int(request.form.get('minimum_stock',2) or 2))
        db.session.add(item); db.session.commit(); flash('Inventory item added.','success'); return redirect(url_for('inventory.stock'))
    return render_template('inventory_add.html')
@inventory_bp.route('/stock')
def stock_alias(): return stock()
