from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from app.auth.routes import auth_bp
    from app.customers.routes import customers_bp
    from app.sales.routes import sales_bp
    from app.surveys.routes import surveys_bp
    from app.quotations.routes import quotations_bp
    from app.inventory.routes import inventory_bp
    from app.installations.routes import installations_bp
    from app.payments.routes import payments_bp
    from app.maintenance.routes import maintenance_bp
    from app.warranties.routes import warranties_bp
    from app.admin.routes import admin_bp
    from app.api.routes import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(customers_bp, url_prefix='/customer')
    app.register_blueprint(sales_bp, url_prefix='/sales')
    app.register_blueprint(surveys_bp, url_prefix='/surveys')
    app.register_blueprint(quotations_bp, url_prefix='/quotations')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(installations_bp, url_prefix='/installations')
    app.register_blueprint(payments_bp, url_prefix='/payments')
    app.register_blueprint(maintenance_bp, url_prefix='/maintenance')
    app.register_blueprint(warranties_bp, url_prefix='/warranties')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return __import__('flask').render_template('index.html')

    with app.app_context():
        db.create_all()
        seed_data()
    return app

# def seed_data():
#     from app.models import SolarPackage, Inventory, User
#     if SolarPackage.query.count() == 0:
#         packages = [
#             SolarPackage(name='3 kW Residential On-Grid', system_type='On-Grid', capacity_kw=3, panels_info='6 × 550 W panels', inverter_info='3 kW On-Grid inverter', battery_info='Not included', description='Bill reduction and net-metering ready.', warranty_years=10, price=525000),
#             SolarPackage(name='5 kW Residential Hybrid', system_type='Hybrid', capacity_kw=5, panels_info='10 × 550 W panels', inverter_info='5 kW Hybrid inverter', battery_info='2 × Lithium batteries', description='Grid connected with battery backup.', warranty_years=10, price=1250000),
#             SolarPackage(name='8 kW Hybrid System', system_type='Hybrid', capacity_kw=8, panels_info='15 × 550 W panels', inverter_info='8 kW Hybrid inverter', battery_info='2 × Lithium batteries', description='High-capacity home backup solution.', warranty_years=10, price=1650000),
#             SolarPackage(name='10 kW Commercial', system_type='On-Grid', capacity_kw=10, panels_info='19 × 550 W panels', inverter_info='10 kW On-Grid inverter', battery_info='Not included', description='Commercial bill reduction solution.', warranty_years=10, price=1750000),
#             SolarPackage(name='20 kW Commercial Hybrid', system_type='Hybrid', capacity_kw=20, panels_info='37 × 550 W panels', inverter_info='20 kW Hybrid inverter', battery_info='Commercial battery bank', description='Commercial backup and generation.', warranty_years=10, price=3400000),
#             SolarPackage(name='50 kW Industrial', system_type='On-Grid', capacity_kw=50, panels_info='91 × 550 W panels', inverter_info='50 kW Industrial inverter', battery_info='Not included', description='Large-scale industrial generation.', warranty_years=10, price=7500000),
#             SolarPackage(name='Agricultural Tube-Well System', system_type='Off-Grid', capacity_kw=15, panels_info='28 × 550 W panels', inverter_info='15 kW Solar pump inverter', battery_info='Optional', description='Solar solution for agricultural pumping.', warranty_years=8, price=2500000),
#         ]
#         db.session.add_all(packages)
#     if Inventory.query.count() == 0:
#         db.session.add_all([
#             Inventory(item_name='550W Mono Solar Panel', category='Solar Panel', brand='Tier-1', model='N-Type 550W', quantity=50, purchase_price=28000, selling_price=35000, minimum_stock=10),
#             Inventory(item_name='5kW Hybrid Inverter', category='Inverter', brand='SolarEase', model='SE-H5', quantity=10, purchase_price=220000, selling_price=275000, minimum_stock=2),
#             Inventory(item_name='Lithium Battery 5kWh', category='Battery', brand='SolarEase', model='LFP-5', quantity=12, purchase_price=180000, selling_price=230000, minimum_stock=2),
#             Inventory(item_name='DC Cable 6mm', category='Cable', brand='Generic', model='PV-6', quantity=200, purchase_price=250, selling_price=350, minimum_stock=30),
#         ])
#     if User.query.filter_by(email='admin@solarease.pk').first() is None:
#         db.session.add(User(full_name='SolarEase Administrator', username='admin', email='admin@solarease.pk', password='admin123', role='admin'))
#     db.session.commit()


def seed_data():
    from app.models import SolarPackage, Inventory, User, Role, Permission

    # 1. New Permissions Seed
    if Permission.query.count() == 0:
        default_permissions = [
            ('view_dashboard', 'View Dashboard', 'General'),
            ('manage_users', 'Manage Staff & Roles', 'Admin'),
            ('view_surveys', 'View Technical Surveys', 'Engineers'),
            ('manage_inventory', 'Manage Stock & Inventory', 'Inventory'),
            ('process_payments', 'Process & View Payments', 'Finance'),
            ('view_installations', 'View Installation Tasks', 'Technician'),
            ('create_quotations', 'Create Sales Quotations', 'Sales')
        ]
        for name, label, cat in default_permissions:
            db.session.add(Permission(name=name, label=label, category=cat))
        db.session.commit()

    # 2. New Staff Roles Seed (Customer Hata Diya Hai)
    if Role.query.count() == 0:
        roles_config = [
            ('sales', 'Sales Representative', 'sales.dashboard', True),
            ('engineer', 'Solar Engineer', 'surveys.engineer_dashboard', True),
            ('technician', 'Installation Technician', 'installations.technician_dashboard', True),
            ('inventory_manager', 'Inventory Manager', 'inventory.stock', True),
            ('finance', 'Finance Officer', 'payments.finance_dashboard', True),
            ('admin', 'Administrator', 'admin.dashboard', True),
        ]
        for name, label, endpoint, is_staff in roles_config:
            db.session.add(Role(name=name, label=label, dashboard_endpoint=endpoint, is_staff=is_staff))
        db.session.commit()

        admin_role = Role.query.filter_by(name='admin').first()
        if admin_role:
            admin_role.permissions = Permission.query.all()
            db.session.commit()

    # 3. Purana Solar Packages Seed (RETAIN THIS - Mat Hatao)
    if SolarPackage.query.count() == 0:
        packages = [
            SolarPackage(name='3 kW Residential On-Grid', system_type='On-Grid', capacity_kw=3, panels_info='6 × 550 W panels', inverter_info='3 kW On-Grid inverter', battery_info='Not included', description='Bill reduction and net-metering ready.', warranty_years=10, price=525000),
            SolarPackage(name='5 kW Residential Hybrid', system_type='Hybrid', capacity_kw=5, panels_info='10 × 550 W panels', inverter_info='5 kW Hybrid inverter', battery_info='2 × Lithium batteries', description='Grid connected with battery backup.', warranty_years=10, price=1250000),
            SolarPackage(name='8 kW Hybrid System', system_type='Hybrid', capacity_kw=8, panels_info='15 × 550 W panels', inverter_info='8 kW Hybrid inverter', battery_info='2 × Lithium batteries', description='High-capacity home backup solution.', warranty_years=10, price=1650000),
            SolarPackage(name='10 kW Commercial', system_type='On-Grid', capacity_kw=10, panels_info='19 × 550 W panels', inverter_info='10 kW On-Grid inverter', battery_info='Not included', description='Commercial bill reduction solution.', warranty_years=10, price=1750000),
            SolarPackage(name='20 kW Commercial Hybrid', system_type='Hybrid', capacity_kw=20, panels_info='37 × 550 W panels', inverter_info='20 kW Hybrid inverter', battery_info='Commercial battery bank', description='Commercial backup and generation.', warranty_years=10, price=3400000),
            SolarPackage(name='50 kW Industrial', system_type='On-Grid', capacity_kw=50, panels_info='91 × 550 W panels', inverter_info='50 kW Industrial inverter', battery_info='Not included', description='Large-scale industrial generation.', warranty_years=10, price=7500000),
            SolarPackage(name='Agricultural Tube-Well System', system_type='Off-Grid', capacity_kw=15, panels_info='28 × 550 W panels', inverter_info='15 kW Solar pump inverter', battery_info='Optional', description='Solar solution for agricultural pumping.', warranty_years=8, price=2500000),
        ]
        db.session.add_all(packages)

    # 4. Purana Inventory Seed (RETAIN THIS - Mat Hatao)
    if Inventory.query.count() == 0:
        db.session.add_all([
            Inventory(item_name='550W Mono Solar Panel', category='Solar Panel', brand='Tier-1', model='N-Type 550W', quantity=50, purchase_price=28000, selling_price=35000, minimum_stock=10),
            Inventory(item_name='5kW Hybrid Inverter', category='Inverter', brand='SolarEase', model='SE-H5', quantity=10, purchase_price=220000, selling_price=275000, minimum_stock=2),
            Inventory(item_name='Lithium Battery 5kWh', category='Battery', brand='SolarEase', model='LFP-5', quantity=12, purchase_price=180000, selling_price=230000, minimum_stock=2),
            Inventory(item_name='DC Cable 6mm', category='Cable', brand='Generic', model='PV-6', quantity=200, purchase_price=250, selling_price=350, minimum_stock=30),
        ])

    # 5. Staff Users Seed (Updated with role_id)
    demo_staff = [
        ('SolarEase Administrator', 'admin', 'admin@solarease.pk', 'admin123'),
        ('Ayesha Khan', 'sales1', 'sales@solarease.pk', 'sales123'),
        ('Bilal Ahmed', 'engineer1', 'engineer@solarease.pk', 'engineer123'),
        ('Usman Tariq', 'technician1', 'technician@solarease.pk', 'technician123'),
        ('Sara Malik', 'inventory1', 'inventory@solarease.pk', 'inventory123'),
        ('Hamza Sheikh', 'finance1', 'finance@solarease.pk', 'finance123'),
    ]
    roles_by_username = {'admin':'admin','sales1':'sales','engineer1':'engineer','technician1':'technician','inventory1':'inventory_manager','finance1':'finance'}
    
    for full_name, username, email, password in demo_staff:
        if User.query.filter_by(email=email).first() is None:
            role_obj = Role.query.filter_by(name=roles_by_username[username]).first()
            user = User(
                full_name=full_name, 
                username=username, 
                email=email, 
                password=password, 
                role=roles_by_username[username],
                role_id=role_obj.id if role_obj else None
            )
            db.session.add(user)
            
    db.session.commit()