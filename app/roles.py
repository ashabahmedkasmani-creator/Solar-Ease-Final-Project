"""
Central definition of the 7 SolarEase roles (per project spec section 3).
Every other module imports from here so the role list only lives in one place.
"""

CUSTOMER = 'customer'
SALES = 'sales'
ENGINEER = 'engineer'
TECHNICIAN = 'technician'
INVENTORY_MANAGER = 'inventory_manager'
FINANCE = 'finance'
ADMIN = 'admin'

ROLES = [CUSTOMER, SALES, ENGINEER, TECHNICIAN, INVENTORY_MANAGER, FINANCE, ADMIN]

# Roles that are staff (created by the Administrator, not self-registered)
STAFF_ROLES = [SALES, ENGINEER, TECHNICIAN, INVENTORY_MANAGER, FINANCE, ADMIN]

ROLE_LABELS = {
    CUSTOMER: 'Customer',
    SALES: 'Sales Representative',
    ENGINEER: 'Solar Engineer',
    TECHNICIAN: 'Installation Technician',
    INVENTORY_MANAGER: 'Inventory Manager',
    FINANCE: 'Finance Officer',
    ADMIN: 'Administrator',
}

# Which endpoint each role should land on right after login / when denied access
ROLE_DASHBOARD_ENDPOINT = {
    CUSTOMER: 'customers.dashboard',
    SALES: 'sales.dashboard',
    ENGINEER: 'surveys.engineer_dashboard',
    TECHNICIAN: 'installations.technician_dashboard',
    INVENTORY_MANAGER: 'inventory.stock',
    FINANCE: 'payments.finance_dashboard',
    ADMIN: 'admin.dashboard',
}


def dashboard_for(role):
    """Returns the endpoint name of the dashboard that belongs to this role."""
    return ROLE_DASHBOARD_ENDPOINT.get(role, 'customers.dashboard')


def label_for(role):
    return ROLE_LABELS.get(role, role.title() if role else 'Unknown')
