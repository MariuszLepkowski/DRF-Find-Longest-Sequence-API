from rest_framework import serializers


class SequenceInputSerializer(serializers.Serializer):
    raw_sequence = serializers.CharField(
        required=True, help_text="Current string to analyze"
    )

    def validate_raw_sequence(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("String cannot be empty")
        return value


class SequenceOutputSerializer(serializers.Serializer):
    input_sequence = serializers.CharField()
    longest_sequence = serializers.CharField()
    length = serializers.IntegerField()
