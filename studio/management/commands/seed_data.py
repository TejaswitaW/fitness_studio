import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from studio.models import Booking, Client, FitnessClass


fake = Faker()


class Command(BaseCommand):
    """
    Django management command to seed the database with fake data for testing and development.

    This command creates:
    - 10 fake clients with unique names and emails.
    - 5 fake fitness classes with random class types, instructors, start times, and available slots.
    - 15 fake bookings assigned randomly to clients and fitness classes, decrementing available slots accordingly.

    Usage:
        python manage.py seed_data
    """

    help = "Seed the database with fake data"

    def handle(self, *args, **kwargs):
        # Create fake clients
        for _ in range(10):
            name = fake.name()
            email = fake.unique.email()
            Client.objects.get_or_create(name=name, email=email)

        # Create fake fitness classes
        class_types = ["Yoga", "Zumba", "HIIT"]
        for _ in range(5):
            FitnessClass.objects.create(
                class_name=random.choice(class_types),
                instructor=fake.name(),
                start_time=timezone.now() + timedelta(days=random.randint(1, 10)),
                available_slots=random.randint(5, 20),
            )

        # Create fake bookings
        clients = list(Client.objects.all())
        classes = list(FitnessClass.objects.all())

        for _ in range(15):
            client = random.choice(clients)
            fitness_class = random.choice(classes)
            if fitness_class.available_slots > 0:
                Booking.objects.create(client=client, fitness_class=fitness_class)
                fitness_class.available_slots -= 1
                fitness_class.save()

        self.stdout.write(self.style.SUCCESS("Fake data successfully seeded!"))
