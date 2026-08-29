from rest_framework import serializers


class SequenceOutputSerializer(serializers.Serializer):
    input_sequence = serializers.CharField()
    longest_sequence = serializers.CharField()
    length = serializers.IntegerField()
