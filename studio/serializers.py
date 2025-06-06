import logging

from django.utils import timezone
from pytz import timezone as pytz_timezone
from rest_framework import serializers

from .models import Booking, Client, FitnessClass


logger = logging.getLogger(__name__)


class GetClientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Client model.

    Serializes the client's name and email for API responses.
    """

    class Meta:
        model = Client
        fields = ["name", "email"]


class CreateFitnessClassSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a FitnessClass instance.

    Handles serialization and validation of the following fields:
    - class_name: Type of the fitness class (e.g., Yoga, Zumba, HIIT).
    - instructor: Name of the instructor.
    - start_time: Scheduled start date and time of the class.
    - available_slots: Number of available booking slots.
    """

    class Meta:
        model = FitnessClass
        fields = ["class_name", "instructor", "start_time", "available_slots"]


class FitnessClassSerializer(serializers.ModelSerializer):
    """
    Serializer for the FitnessClass model.

    Includes a custom read-only field `start_time_local` which converts
    the `start_time` of the class to the timezone specified in the request's
    query parameters. Defaults to the server's timezone if none provided.

    Fields:
    - id: Unique identifier of the fitness class.
    - class_name: Name/type of the fitness class (e.g., Yoga, Zumba, HIIT).
    - instructor: Name of the instructor.
    - start_time_local: Localized start time of the class as per the requested timezone.
    - available_slots: Number of available slots for booking.
    """

    start_time_local = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = [
            "id",
            "class_name",
            "instructor",
            "start_time_local",
            "available_slots",
        ]

    def get_start_time_local(self, obj):
        """
        Convert the `start_time` to the timezone provided in the request query parameter `timezone`.

        If no timezone is provided, defaults to the server's timezone.

        Logs the conversion for debugging purposes.
        """
        request = self.context.get("request")
        tz_param = request.query_params.get("timezone") if request else None
        tz = pytz_timezone(tz_param) if tz_param else timezone.get_default_timezone()
        logger.debug(f"Converting start_time '{obj.start_time}' to timezone '{tz}'")
        return obj.start_time.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S %Z")


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for handling Booking creation requests.

    This serializer accepts the following write-only fields:
    - class_id: ID of the FitnessClass to book.
    - client_name: Name of the client making the booking.
    - client_email: Email of the client making the booking.

    Validation:
    - Ensures the FitnessClass with the given class_id exists.
    - Checks if there are available slots in the requested FitnessClass.

    Creation:
    - Fetches or creates a Client based on the provided email and name.
    - Decrements the available slots count for the FitnessClass.
    - Creates a Booking associating the Client and FitnessClass.

    Logging is used extensively to track validation failures, client creation,
    slot decrementing, and booking creation.
    """

    class_id = serializers.IntegerField(
        write_only=True,
        required=True,
        error_messages={
            "required": "class_id is required.",
            "invalid": "class_id must be a valid integer.",
        },
    )
    client_name = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        error_messages={"blank": "client_name cannot be blank."},
    )
    client_email = serializers.EmailField(
        write_only=True,
        required=True,
        allow_blank=False,
        error_messages={"blank": "client_email cannot be blank."},
    )

    class Meta:
        model = Booking
        fields = ["class_id", "client_name", "client_email"]

    def validate(self, data):
        """
        Validate that the specified FitnessClass exists and has available slots.

        Raises ValidationError if:
        - FitnessClass does not exist.
        - No available slots remain.

        Logs warnings and info messages accordingly.
        """
        class_id = data.get("class_id")
        if not class_id:
            logger.warning("Validation failed: class_id is missing in the request.")
            raise serializers.ValidationError("class_id is required.")
        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
        except FitnessClass.DoesNotExist:
            logger.warning(
                f"Validation failed: Fitness class with ID {class_id} does not exist."
            )
            raise serializers.ValidationError("Fitness class does not exist.")

        if fitness_class.available_slots <= 0:
            logger.info(
                f"No slots available for class ID {class_id} ({fitness_class.class_name})."
            )
            raise serializers.ValidationError("No slots available.")

        return data

    def create(self, validated_data):
        """
        Create a Booking instance after:
        - Fetching the FitnessClass.
        - Creating or retrieving the Client.
        - Decrementing the available slots for the FitnessClass.
        - Creating the Booking object.

        Logs detailed info and debug messages throughout the process.
        """
        class_id = validated_data.get("class_id")
        client_email = validated_data.get("client_email")
        client_name = validated_data.get("client_name")

        fitness_class = FitnessClass.objects.get(id=class_id)
        logger.debug(
            f"Fetched FitnessClass ID {class_id}: {fitness_class.class_name} with {fitness_class.available_slots} slots remaining."
        )
        client, created = Client.objects.get_or_create(
            email=client_email,
            defaults={"name": client_name},
        )
        if created:
            logger.info(f"New client created: {client_name} ({client_email})")
        else:
            logger.debug(f"Existing client found: {client_name} ({client_email})")

        fitness_class.available_slots -= 1
        fitness_class.save()
        logger.info(
            f"Decremented slot for class '{fitness_class.class_name}'. Remaining slots: {fitness_class.available_slots}"
        )
        booking = Booking.objects.create(fitness_class=fitness_class, client=client)
        logger.info(
            f"Booking created: Client '{client.name}' booked '{fitness_class.class_name}' on {fitness_class.start_time}"
        )
        return booking


class BookingReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Booking details.

    Includes:
    - Nested fitness_class details serialized by FitnessClassSerializer.
    - Client's email address accessed via the related Client model.

    Fields:
    - id: Booking identifier.
    - fitness_class: Serialized fitness class information.
    - client_email: Email of the client who made the booking (read-only).
    """

    fitness_class = FitnessClassSerializer()
    client_email = serializers.EmailField(source="client.email", read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "fitness_class", "client_email"]
