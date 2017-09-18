from .models import *
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DynamicDocumentSerializer


class DataSourceSerializer(DynamicDocumentSerializer):
    """
    Serializing all Data Sources
    """

    class Meta:
        model = DataSource
        fields = '__all__'
        #fields = ('id', 'name', 'supplier')


class FeatureSerializer(DynamicDocumentSerializer):
    """
    Serializing all Data Sources
    """

    class Meta:
        model = DataSource
        fields = '__all__'



class SpeciesSerializer(DynamicDocumentSerializer):
    """
    Serializing all Data Sources
    """

    class Meta:
        model = DataSource
        fields = '__all__'
