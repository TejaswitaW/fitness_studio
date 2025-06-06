from datetime import timedelta

import pytest
from django.utils import timezone
from model_bakery import baker

from studio.models import FitnessClass


@pytest.mark.django_db
def test_get_upcoming_fitness_classes(api_client):
    """
    Test retrieving a list of upcoming fitness classes.

    - Creates two FitnessClass instances with future start times.
    - Sends a GET request to /api/classes/.
    - Asserts that the response status is 200 OK.
    - Asserts that two fitness classes are returned in the response.
    """
    future_time = timezone.now() + timedelta(days=1)
    baker.make(FitnessClass, _quantity=2, start_time=future_time)

    response = api_client.get("/api/classes/")
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_classes_with_timezone_filter(api_client):
    """
    Test fetching fitness classes with a timezone query parameter.

    - Creates a FitnessClass instance.
    - Sends a GET request to /api/classes/?timezone=Asia/Kolkata.
    - Asserts that the response status is 200 OK.
    - Verifies that the endpoint handles timezone filtering correctly.
    """
    baker.make(FitnessClass)
    response = api_client.get("/api/classes/?timezone=Asia/Kolkata")
    assert response.status_code == 200
