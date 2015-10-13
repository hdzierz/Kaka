from .models import *
from rest_framework import serializers

class TargetSerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """

    class Meta:
        model = Target
        fields = ('obid', 'obs')



class GeneSerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """
    class Meta:
        model = Gene
        fields = ('obid', 'obs')

