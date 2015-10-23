from .models import *
from rest_framework import serializers


class TreeSerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """
    class Meta:
        model = Tree
        fields = ('obid', 'obs')


class FishSerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """
    class Meta:
        model = Fish
        fields = ('obid', 'obs')


