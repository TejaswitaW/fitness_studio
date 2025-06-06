import pytest
from model_bakery import baker

from studio.models import Booking, Client, FitnessClass


@pytest.mark.django_db
def test_successful_booking(api_client):
    """
    Test creating a successful booking for a fitness class with available slots.

    - Creates a FitnessClass with 5 available slots.
    - Posts booking data to the /api/book/ endpoint.
    - Asserts that the response status is 201 Created.
    - Checks that exactly one Booking object is created in the database.
    """
    fitness_class = baker.make(FitnessClass, available_slots=5)
    payload = {
        "class_id": fitness_class.id,
        "client_name": "Alice",
        "client_email": "alice@example.com",
    }
    response = api_client.post("/api/book/", payload, format="json")
    assert response.status_code == 201
    assert Booking.objects.count() == 1


@pytest.mark.django_db
def test_booking_with_no_slots(api_client):
    """
    Test that booking fails if the fitness class has no available slots.

    - Creates a FitnessClass with 0 available slots.
    - Attempts to book the class.
    - Asserts the response status is 400 Bad Request.
    - Confirms the error message contains 'No slots available'.
    """
    fitness_class = baker.make(FitnessClass, available_slots=0)
    payload = {
        "class_id": fitness_class.id,
        "client_name": "Bob",
        "client_email": "bob@example.com",
    }
    response = api_client.post("/api/book/", payload, format="json")
    assert response.status_code == 400
    assert "No slots available" in str(response.data)


@pytest.mark.django_db
def test_get_bookings_by_email(api_client):
    """
    Test retrieving bookings filtered by client email.

    - Creates a Client with a specific email.
    - Creates 2 bookings associated with that client.
    - Sends GET request to /api/bookings/?email=<email>.
    - Asserts the response status is 200 OK.
    - Confirms exactly 2 bookings are returned.
    """
    client = baker.make(Client, email="test@example.com")
    baker.make(Booking, client=client, _quantity=2)
    response = api_client.get("/api/bookings/?email=test@example.com")
    assert response.status_code == 200
    assert len(response.data) == 2
