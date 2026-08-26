import requests
from django.conf import settings


class ExternalAPIError(Exception):
    """Raised when the external API cannot be reached."""


class ExternalAPIClient:
    def get_data(self) -> str:
        try:
            response = requests.get(
                settings.EXTERNAL_API_URL,
                timeout=5,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ExternalAPIError from exc

        return response.text
