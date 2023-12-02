from django.urls import path
from reservation.views import CreateTicketAPI, GetTicketAPI, CancelTicketAPI

urlpatterns = [
    path("ticket", CreateTicketAPI.as_view(), name="create-ticket-api"),
    path("ticket/<int:ticket_id>", GetTicketAPI.as_view(), name="get-ticket-api"),
    path("ticket/cancel/<int:ticket_id>", CancelTicketAPI.as_view(), name="cancel-ticket-api"),
]
