from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.clients import ExternalAPIClient, ExternalAPIError
from core.serializers import SequenceOutputSerializer
from core.services import find_longest_sequence


class ProcessDataAPIView(APIView):
    def get(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        try:
            raw_sequence = ExternalAPIClient.get_data()
        except ExternalAPIError:
            return Response(
                {"error": "Failed to retrieve data from external API."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

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
