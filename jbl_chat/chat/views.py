from django.utils import timezone


from django.db.models import Q
from django.shortcuts import render

from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from .models import Message
from datetime import timedelta
from django.contrib.auth.decorators import login_required






User = get_user_model()

@login_required
def home_view(request):
    return render(request, 'base.html', {})

@login_required
def messages_with(request, other_user_id):

    user = request.user
    # Retrieve messages where the user is either the sender or the recipient - currently ordered by newest
    messages =  Message.objects.filter(
        Q(sender=user, recipient_id=other_user_id) | Q(sender_id=other_user_id, recipient=user)
    ).order_by('sent_at')

    # Format the current date as "Y-m-d"
    today_date = timezone.now().strftime('%Y-%m-%d')
    week_ago = timezone.now() - timedelta(days=7)


    context = {
        'messages': messages,
        'other_user_id': other_user_id,
        'today_date': today_date,
        'week_ago': week_ago,
        'messages': messages,
    }
    return render(request, 'base.html#messages-list', context)


@login_required
def new_messages_with(request, other_user_id):

    user = request.user
    # Retrieve messages where the user is either the sender or the recipient - currently ordered by newest
    messages =  Message.objects.filter(
        Q(sender=user, recipient_id=other_user_id) | Q(sender_id=other_user_id, recipient=user)
    ).order_by('sent_at')

    # Format the current date as "Y-m-d"
    today_date = timezone.now().strftime('%Y-%m-%d')
    week_ago = timezone.now() - timedelta(days=7)


    context = {
        'messages': messages,
        'other_user_id': other_user_id,
        'today_date': today_date,
        'week_ago': week_ago,
        'messages': messages,
    }
    return render(request, 'base.html#messages', context)

@login_required
def add_message(request):
    if request.method == "POST":
        recipient_id = request.POST.get("recipient")
        if not recipient_id:
            return HttpResponseBadRequest("Missing recipient id")

        try:
            recipient = User.objects.get(pk=recipient_id)
        except User.DoesNotExist:
            return HttpResponseBadRequest("Invalid recipient")

        content = request.POST.get("content", "").strip()

        # Fetch the latest message between the two users.
        latest_message = Message.objects.filter(
            Q(sender=request.user, recipient=recipient) |
            Q(sender=recipient, recipient=request.user)
        ).only("sent_at").last()

        # Determine if a new header is needed.
        if latest_message:
            needs_today_header = latest_message.sent_at.date() != timezone.localdate()
        else:
            needs_today_header = True

        message = Message.objects.create(
            content=content,
            sender=request.user,
            recipient=recipient
        )
        # Return a partial template snippet for HTMX to swap into the page.
        return render(request, "base.html#message", {"message": message, 'swap_oob_message_add_form': True, 'needs_today_header': needs_today_header,  'other_user_id': recipient_id})
    # On GET, render the full page with the form.
    return render(request, "base.html#message-add")