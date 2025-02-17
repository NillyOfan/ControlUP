import requests
import yaml
import os
import logging
from urllib.parse import urlparse
from tests.conftest import config

logger = logging.getLogger(__name__)


class APIClient:
    """A generic API client to interact with REST APIs."""

    def __init__(self, base_url=None):
        """Initialize the API client with a base URL and verify its reachability."""
        self.base_url = base_url or config["api"]["base_url"]
        self.session = requests.Session()

        logging.debug(f"APIClient initialized with base URL: {self.base_url}")

    @staticmethod
    def _is_valid_url(url):
        """Check if the URL is valid (basic format validation)."""
        parsed = urlparse(url)
        return bool(parsed.scheme and parsed.netloc)

    def _is_url_reachable(self, url, timeout=5):
        """Check if the given API URL is reachable with retries."""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()  # Raises an error for 4xx and 5xx responses
            return True

        except requests.exceptions.ConnectionError as e:
            logging.error(f"DNS resolution failed or server unreachable: {e}")
        except requests.exceptions.Timeout:
            logging.error(f"Timeout reached when connecting to: {url}")
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error {e.response.status_code}: {e}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Unexpected error: {e}")

        return False  # Return False if the API is unreachable

    def get(self, endpoint, params=None, headers=None):
        """Send a GET request and return the response."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url} | Params: {params}")
        response = self.session.get(url, params=params, headers=headers)
        self._log_response(response)
        return response

    def post(self, endpoint, data=None, json=None, headers=None):
        """Send a POST request and return the response."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url} | Data: {json or data}")
        response = self.session.post(url, data=data, json=json, headers=headers)
        self._log_response(response)
        return response

    def _log_response(self, response):
        """Logs the response status and content."""
        logger.debug(f"Response [{response.status_code}]: {response.text}")


class AirportGapClient(APIClient):
    """Specialized API client for AirportGapClient."""

    def __init__(self, base_url=None):
        """Initialize the AirportGap client and verify the /airports endpoint exists."""
        super().__init__(base_url)  # Validate the base URL first

        if not self._is_valid_url(self.base_url):
            raise ValueError(f"Invalid URL provided: {self.base_url}")

        test_url = f"{self.base_url}/airports"
        if not self._is_url_reachable(test_url):
            raise ConnectionError(f"AirportGap API is unreachable at: {test_url}")

        logging.debug(f"AirportGapClient initialized with base URL: {self.base_url}")

    def get_airports(self):
        """Fetch the list of airports."""
        response = self.get("/airports")
        return response.json()

    def calculate_distance(self, from_code, to_code):
        """Calculate the distance between two airports."""
        payload = {"from": from_code, "to": to_code}
        response = self.post("/airports/distance", json=payload)
        return response.json()
