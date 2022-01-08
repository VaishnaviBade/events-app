from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import get_user_model

User = get_user_model()


# @login_required
def events_page(request):
    all_events = Event.objects.all()
    context = {"all_events": all_events}
    return render(request, "events.html", context)


@login_required
def my_events(request):
    my_events = Event.objects.filter(created_by=request.user)
    print("my_events", my_events)
    context = {"my_events": my_events}
    return render(request, "my_events.html", context)


@login_required
def create_event_page(request):
    event_form = EventForm(request.POST or None, request.FILES or None)
    if event_form.is_valid():
        edit_event_form = event_form.save(commit=False)
        edit_event_form.created_by = request.user
        event_form.save()
        messages.info(request, f"Event Created Successfully !!")
        return redirect("my_events")

    context = {"event_form": event_form}
    return render(request, "create_event.html", context)


@login_required
def update_event_page(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    if request.user == event_obj.created_by:
        event_form = EventForm(
            request.POST or None, request.FILES or None, instance=event_obj
        )
        if event_form.is_valid():
            edit_event_form = event_form.save(commit=False)
            edit_event_form.created_by = request.user
            event_form.save()
            messages.info(request, f"Your Event Updated Successfully !!")
            return redirect("my_events")

        context = {"event_form": event_form, "event_obj": event_obj}
        return render(request, "update_event.html", context)
    else:
        messages.info(request, f"You Not have permission to update!!")
        return redirect("my_events")


@login_required
def toggle_like_unlink_event(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    print("ple like my post from", event_obj)
    if request.user in event_obj.like_people.all():
        event_obj.like_people.remove(request.user)
        action = "unlike"

    else:
        event_obj.like_people.add(request.user)
        action = "like"

    event_obj.save()
    return JsonResponse(
        {"success": True, "action": action, "num_likes": event_obj.get_number_like()},
        safe=False,
    )
