from .models import *
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DynamicDocumentSerializer

class MarkerSerializer(DynamicDocumentSerializer):
    """
    Serializing all the Authors
    """

    class Meta:
        model = Marker
        fields = '__all__'



class PrimerSerializer(DynamicDocumentSerializer):
    """
    Serializing all the Authors
    """
    class Meta:
        model = Primer
        fields = '__all__'

