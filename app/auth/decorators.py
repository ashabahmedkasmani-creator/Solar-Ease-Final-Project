from functools import wraps
from flask import session, redirect, url_for, flash, request


def login_required(f):
    """Blocks the view unless a user_id exists in the session."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return wrapper


def role_required(*roles):
    """Blocks the view unless the session role is one of the given roles.
    Also enforces login first, so it can be used on its own."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not session.get('user_id'):
                flash('Please log in to continue.', 'warning')
                return redirect(url_for('auth.login', next=request.path))
            if session.get('role') not in roles:
                flash('You do not have permission to view that page.', 'danger')
                return redirect(url_for('customers.dashboard'))
            return f(*args, **kwargs)
        return wrapper
    return decorator
