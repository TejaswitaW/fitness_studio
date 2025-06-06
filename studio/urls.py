from django.urls import path

from .views import BookFitnessClass, BookingListByEmail, FitnessClassList, GetClientList


urlpatterns = [
    path("classes/", FitnessClassList.as_view(), name="class-list"),
    path("book/", BookFitnessClass.as_view(), name="book-class"),
    path("bookings/", BookingListByEmail.as_view(), name="booking-list"),
    path("clients/", GetClientList.as_view(), name="client-list"),
]
