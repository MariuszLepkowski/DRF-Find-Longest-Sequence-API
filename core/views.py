import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import (
    SequenceInputSerializer,
    SequenceOutputSerializer,
)
from core.services import find_longest_sequence


class ProcessDataAPIView(APIView):
    serializer_class = SequenceInputSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        raw_sequence = serializer.validated_data["raw_sequence"]

        return self._build_response(raw_sequence)

    def get(self, request, *args, **kwargs):
        try:
            response = requests.get(
                settings.EXTERNAL_API_URL,
                timeout=5,
            )
            response.raise_for_status()

        except requests.RequestException:
            return Response(
                {"error": ("Failed to retrieve data from external API.")},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return self._build_response(response.text)

    @staticmethod
    def _build_response(raw_sequence: str) -> Response:
        result = find_longest_sequence(raw_sequence)

        output = SequenceOutputSerializer(
            data={
                "input_sequence": raw_sequence,
                "longest_sequence": result,
                "length": len(result),
            }
        )

        output.is_valid(raise_exception=True)

        return Response(output.data)
