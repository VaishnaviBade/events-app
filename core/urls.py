from django.urls import path
from .views import (
    events_page,
    create_event_page,
    my_events,
    toggle_like_unlink_event,
    update_event_page,
)

urlpatterns = [
    path("events/", events_page, name="events_page"),
    path("my-events/", my_events, name="my_events"),
    path(
        "toggle-like-unlink-event/<int:event_id>/",
        toggle_like_unlink_event,
        name="toggle_like_unlink_event",
    ),
    path(
        "update-event/<int:event_id>/",
        update_event_page,
        name="update_event_page",
    ),
    path("create-event/", create_event_page, name="create_event_page"),
]
