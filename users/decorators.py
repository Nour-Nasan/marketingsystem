from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth.decorators import login_required

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'role') and request.user.role == role:
                return view_func(request, *args, **kwargs)
            return redirect('users:error_403')
        return _wrapped_view
    return decorator


admin_required = role_required('admin')
seller_required = role_required('seller')
buyer_required = role_required('buyer')
bazar_organizer_required = role_required('bazar_organizer')
