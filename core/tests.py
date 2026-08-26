from unittest.mock import patch

import pytest
from rest_framework.test import APIClient

from core.clients import ExternalAPIClient, ExternalAPIError
from core.services import find_longest_sequence


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("11199922233475599999", "99999"),
        ("aabbcc", "aa"),
        ("abcdef", "a"),
        ("11111", "11111"),
        ("a", "a"),
        ("", ""),
        (None, ""),
    ],
)
def test_find_longest_sequence(input_data, expected_output):
    assert find_longest_sequence(input_data) == expected_output


@pytest.fixture
def api_client():
    return APIClient()


class TestProcessDataAPI:
    def test_post_success(self, api_client):
        response = api_client.post(
            "/api/process/",
            data={"raw_sequence": "111999922"},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["longest_sequence"] == "9999"
        assert response.data["length"] == 4

    def test_post_invalid_data_returns_400(self, api_client):
        response = api_client.post(
            "/api/process/",
            data={"raw_sequence": "   "},
            format="json",
        )

        assert response.status_code == 400
        assert "raw_sequence" in response.data

    def test_get_external_api_success(self, api_client):
        with patch("core.views.ExternalAPIClient.get_data") as mock_get_data:
            mock_get_data.return_value = "7777722"

            response = api_client.get("/api/process/")

        assert response.status_code == 200
        assert response.data["longest_sequence"] == "77777"
        assert response.data["length"] == 5

    def test_get_external_api_failure(self, api_client):
        with patch("core.views.ExternalAPIClient.get_data") as mock_get_data:
            mock_get_data.side_effect = ExternalAPIError

            response = api_client.get("/api/process/")

        assert response.status_code == 502
        assert response.data["error"] == (
            "Failed to retrieve data from external API."
        )


class TestExternalAPIClient:
    @patch("core.clients.requests.get")
    def test_get_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "7777722"

        client = ExternalAPIClient()

        assert client.get_data() == "7777722"