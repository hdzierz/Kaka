from .models import *
from rest_framework import serializers

class DataSourceSerializer(serializers.ModelSerializer):
    """
    Serializing all Data Sources
    """

    class Meta:
        model = DataSource
        fields = ('id', 'name', 'supplier')



