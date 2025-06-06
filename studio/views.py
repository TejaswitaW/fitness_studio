import logging

from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response

from .models import Booking, Client, FitnessClass
from .serializers import (
    BookingReadSerializer,
    BookingSerializer,
    CreateFitnessClassSerializer,
    FitnessClassSerializer,
    GetClientSerializer,
)


logger = logging.getLogger(__name__)


class GetClientList(generics.ListAPIView):
    """
    API view to retrieve a list of all registered clients.

    Uses the GetClientSerializer to serialize Client instances.
    Logs an info message whenever the client list is fetched.

    Returns:
        Queryset of all Client objects.
    """

    serializer_class = GetClientSerializer

    def get_queryset(self):
        logger.info("Fetching list of all registered clients.")
        return Client.objects.all()


class CreateFitnessClass(generics.CreateAPIView):
    """
    API view to create a new fitness class.

    Uses CreateFitnessClassSerializer for input validation and serialization.
    Logs an info message after successfully creating a new fitness class.

    Methods:
        perform_create(serializer):
            Saves the serializer and logs details about the created fitness class.
    """

    serializer_class = CreateFitnessClassSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            f"New fitness class created: {instance.class_name} by instructor {instance.instructor} on {instance.start_time}"
        )


class FitnessClassList(generics.ListAPIView):
    """
    API view to list all upcoming fitness classes.

    Filters fitness classes whose start_time is greater than or equal to the current time,
    ordering them by start_time in ascending order.

    Logs an info message indicating the time filter being applied.

    The serializer context includes the current request for timezone-aware serialization.

    Methods:
        get_queryset():
            Returns queryset of upcoming fitness classes.

        get_serializer_context():
            Provides additional context (request) to the serializer.
    """

    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        current_time = timezone.now()
        logger.info(f"Fetching upcoming fitness classes starting after {current_time}")
        return FitnessClass.objects.filter(start_time__gte=current_time).order_by(
            "start_time"
        )

    def get_serializer_context(self):
        return {"request": self.request}


class BookFitnessClass(generics.CreateAPIView):
    """
    API view to handle booking a fitness class.

    Uses BookingSerializer to validate and create a new booking record.
    Logs an info message upon successful booking creation indicating
    the client name, class name, and class start time.

    Methods:
        perform_create(serializer):
            Saves the booking instance and logs booking details.
    """

    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        logger.info(
            f"Booking created: Client '{booking.client.name}' booked '{booking.fitness_class.class_name}' on {booking.fitness_class.start_time}"
        )


class BookingListByEmail(generics.ListAPIView):
    """
    API view to list all bookings made by a specific client email.

    Expects an 'email' query parameter in the request URL.
    If no email is provided, returns an empty queryset and logs a warning.
    Otherwise, returns bookings filtered by the client's email, ordered by newest first.

    Methods:
        get_queryset():
            Retrieves the queryset of bookings for the specified client email.
    """

    serializer_class = BookingReadSerializer

    def get_queryset(self):
        email = self.request.query_params.get("email")
        if not email:
            logger.warning("No email query parameter provided in request.")
            return Booking.objects.none()
        logger.info(f"Fetching bookings for client email: {email}")
        return Booking.objects.filter(client__email=email).order_by("-id")
