# SolarEase

Flask-based Solar Panel Installation and Maintenance Service Platform.

## Functional demonstration flow
1. Register / Login
2. Customer dashboard
3. Solar requirement calculation using fixed engineering formulas
4. Compare On-Grid / Off-Grid / Hybrid systems
5. Browse solar packages
6. Book a technical site survey
7. Admin updates survey engineer/status/recommended kW
8. Generate quotation
9. Approve or reject quotation
10. Record payment and create installation project
11. Track installation stages
12. Monitor inventory and low stock
13. View warranty records
14. Submit maintenance requests
15. Admin dashboard and REST API

## Run
```bash
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000/

Demo admin: `admin@solarease.pk` / `admin123`

The SQLite database is created automatically at `instance/solarease.db`.

## Main folders
- `app/auth` authentication
- `app/customers` customer dashboard
- `app/sales` packages and system types
- `app/surveys` survey booking/report update
- `app/quotations` engineering calculator and quotations
- `app/payments` payment records
- `app/installations` installation scheduling/tracking
- `app/inventory` stock management
- `app/warranties` warranty records
- `app/maintenance` support requests
- `app/admin` administration dashboard
- `app/api` REST endpoints
- `app/models` SQLAlchemy database models
- `app/templates` flat template structure

## Important
This is a student/demo implementation based on the supplied SolarEase requirements. External payment gateways, real cloud deployment, Docker/production PostgreSQL, and full multi-role staff workflows are not connected to third-party services.
