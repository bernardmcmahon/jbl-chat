from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

User = get_user_model()

@login_required
def other_users(request):
    other_users = User.objects.filter(is_staff=False).exclude(id=request.user.id)
    context = {
        'other_users': other_users,
    }
    return render(request, 'base.html#conversation-menu', context)

from django.contrib.auth import login, get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden


@login_required
def login_as_user(request, user_id):
    # For safety, only allow superusers to use this view.
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to perform this action.")

    # Retrieve the target user
    user = get_object_or_404(get_user_model(), pk=user_id)

    # Manually set the backend attribute if not already set.
    # This is needed so that Django's login function can correctly authenticate the user.
    if not hasattr(user, 'backend'):
        user.backend = 'django.contrib.auth.backends.ModelBackend'

    login(request, user)
    return redirect('/')  # Redirect to the homepage or any appropriate URL.