from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.clients import ExternalAPIClient, ExternalAPIError
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
        client = ExternalAPIClient()

        try:
            raw_sequence = client.get_data()
        except ExternalAPIError:
            return Response(
                {"error": "Failed to retrieve data from external API."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return self._build_response(raw_sequence)

    @staticmethod
    def _build_response(raw_sequence: str) -> Response:
        result = find_longest_sequence(raw_sequence)

        serializer = SequenceOutputSerializer(
            data={
                "input_sequence": raw_sequence,
                "longest_sequence": result,
                "length": len(result),
            }
        )
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
