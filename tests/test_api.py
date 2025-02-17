import pytest
from utilities.api_client import AirportGapClient
import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def api_client():
    """Fixture to initialize the AirportGap API client."""
    return AirportGapClient()


def test_airport_count(api_client):
    """Verify that the API returns exactly 30 airports."""
    logger.info("Fetching airport list from API")
    response = api_client.get_airports()

    assert response is not None, "Response should not be None"
    assert "data" in response, "Response should contain 'data' field"
    assert len(response["data"]) == 30, f"Expected 30 airports, but got {len(response['data'])}"


def test_specific_airports(api_client):
    """Verify that specific airports exist in the response."""
    logger.info("Fetching airport list to check specific airports")
    response = api_client.get_airports()

    expected_airports = {"Akureyri Airport", "St. Anthony Airport", "CFB Bagotville"}
    actual_airports = {airport["attributes"]["name"] for airport in response["data"]}

    missing_airports = expected_airports - actual_airports
    assert not missing_airports, f"Missing expected airports: {missing_airports}"


def test_airport_distance(api_client):
    """Verify that the distance between KIX and NRT is greater than 400 km."""
    logger.info("Calculating distance between KIX and NRT")
    response = api_client.calculate_distance("KIX", "NRT")

    assert response is not None, "Response should not be None"
    assert "data" in response, "Response should contain 'data' field"
    assert "attributes" in response["data"], "Response should contain 'attributes' field"

    distance_km = response["data"]["attributes"]["kilometers"]
    assert distance_km > 400, f"Expected distance > 400 km, but got {distance_km} km"
