from unittest.mock import patch

import pytest
import requests
from rest_framework.test import APIClient

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
def test_find_longest_sequence_cases(input_data, expected_output):
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

    @patch("core.views.requests.get")
    def test_get_external_api_success(self, mock_get, api_client):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "7777722"

        response = api_client.get("/api/process/")

        assert response.status_code == 200
        assert response.data["longest_sequence"] == "77777"
        assert response.data["length"] == 5

    @patch("core.views.requests.get")
    def test_get_external_api_failure_returns_502(self, mock_get, api_client):
        mock_get.side_effect = requests.RequestException("Timeout error")

        response = api_client.get("/api/process/")

        assert response.status_code == 502
        assert "error" in response.data
