"""
URL configuration for the Studio app.

This module defines the API endpoints for managing fitness classes, bookings, and clients.

Endpoints:
-----------
- /classes/   : Lists upcoming fitness classes. (GET)
- /book/      : Allows clients to book a fitness class. (POST)
- /bookings/  : Retrieves bookings filtered by client email. (GET)
- /clients/   : Lists all registered clients. (GET)

Each endpoint is connected to its corresponding class-based view in the `views.py` module.
"""
from django.urls import path

from .views import BookFitnessClass, BookingListByEmail, FitnessClassList, GetClientList


urlpatterns = [
    path("classes/", FitnessClassList.as_view(), name="class-list"),
    path("book/", BookFitnessClass.as_view(), name="book-class"),
    path("bookings/", BookingListByEmail.as_view(), name="booking-list"),
    path("clients/", GetClientList.as_view(), name="client-list"),
]
