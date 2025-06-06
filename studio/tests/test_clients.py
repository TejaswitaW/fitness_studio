import pytest
from model_bakery import baker

from studio.models import Client


@pytest.mark.django_db
def test_get_all_clients(api_client):
    """
    Test retrieving the list of all registered clients.

    This test uses model_bakery to create 3 dummy Client instances,
    then sends a GET request to the /api/clients/ endpoint.

    Asserts:
        - The response status code is 200 (OK).
        - The response contains exactly 3 clients.
    """
    baker.make(Client, _quantity=3)
    response = api_client.get("/api/clients/")
    assert response.status_code == 200
    assert len(response.data) == 3
