from django.db import models
from django.utils import timezone


class Client(models.Model):
    """
    Represents a client who books fitness classes.

    Stores the client's name and a unique email address used for identification
    and communication. One client can book multiple fitness classes.
    """

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)


class FitnessClass(models.Model):
    """
    Represents a fitness class offered by the studio.

    Attributes:
        class_name (str): The type of fitness class (e.g., Yoga, Zumba, HIIT).
        instructor (str): Name of the instructor conducting the class.
        available_slots (int): Number of spots available for clients to book.
        start_time (datetime): Date and time when the class starts.
    """

    CLASS_CHOICES = [("Yoga", "Yoga"), ("Zumba", "Zumba"), ("HIIT", "HIIT")]
    class_name = models.CharField(choices=CLASS_CHOICES, max_length=20)
    instructor = models.CharField(max_length=100)
    available_slots = models.PositiveIntegerField()
    start_time = models.DateTimeField(default=timezone.now)


class Booking(models.Model):
    """
    Represents a booking made by a client for a specific fitness class.

    Attributes:
        fitness_class (ForeignKey): The fitness class that is booked.
        client (ForeignKey): The client who made the booking.

    The `related_name="bookings"` on client allows reverse lookup of all bookings by a client.
    """

    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="bookings"
    )

    def __str__(self):
        return f"{self.client.name} booked {self.fitness_class}"
