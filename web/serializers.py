from django.forms import widgets
from rest_framework import serializers
from api.models import *


class FishObSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)

    form_completed = serializers.BooleanField(default=False)
    values = serializers.CharField(max_length=1024)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return FishOb.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.form_completed = validated_data.get('form_completed', instance.form_completed)
        instance.values = validated_data.get('values', instance.values)
        instance.save()
        return instance
