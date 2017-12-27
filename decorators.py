from flask import redirect
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from functools import wraps

__all__ = ["login_required", "admin_required", "teacher_required", "templated"]

def admin_required(f):
    @wraps(f)

    @login_required
    def dec_f(*args, **kwargs):
        if current_user.is_admin:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("dashboard"))

    return dec_f

def teacher_required(f):
    @wraps(f)

    @login_required
    def dec_f(*args, **kwargs):
        if current_user.is_teacher or current_user.is_admin:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("dashboard"))

    return dec_f
    
from flask import request, render_template

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator
