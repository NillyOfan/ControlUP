import requests
import yaml
import os
from utilities.logger import logger


# Get the absolute path to the config file
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.yaml")
config_path = os.path.abspath(config_path)  # Ensures absolute path

if not os.path.exists(config_path):
    raise FileNotFoundError(f"Configuration file not found: {config_path}")

# Load configuration
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

class APIClient:
    """A generic API client to interact with REST APIs."""

    # Example usage in tests:
    # api_client = APIClient()
    # response = api_client.get("/api/airports")

    def __init__(self, base_url=None):
        """Initialize the API client with a base URL."""
        self.base_url = base_url or config["api"]["base_url"]
        self.session = requests.Session()

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
    """Specialized API client for Airport."""

    def __init__(self):
        super().__init__(base_url=config["api"]["base_url"])  # Uses the generic APIClient

    def get_airports(self):
        """Fetch the list of airports."""
        response = self.get("/airports")
        return response.json()

    def calculate_distance(self, from_code, to_code):
        """Calculate the distance between two airports."""
        payload = {"from": from_code, "to": to_code}
        response = self.post("/airports/distance", json=payload)
        return response.json()
