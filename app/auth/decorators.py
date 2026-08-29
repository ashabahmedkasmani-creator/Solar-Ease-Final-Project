from functools import wraps
from flask import session, redirect, url_for, flash, request
from app.roles import dashboard_for


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
    Also enforces login first, so it can be used on its own.
    'admin' always has access regardless of which roles are listed, since
    the Administrator is allowed to manage every module."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not session.get('user_id'):
                flash('Please log in to continue.', 'warning')
                return redirect(url_for('auth.login', next=request.path))
            role = session.get('role')
            if role not in roles and role != 'admin':
                flash('You do not have permission to view that page. That module belongs to a different role.', 'danger')
                return redirect(url_for(dashboard_for(role)))
            return f(*args, **kwargs)
        return wrapper
    return decorator
