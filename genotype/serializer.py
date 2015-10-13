from .models import *
from rest_framework import serializers

class MarkerSerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """

    def get_data():
        data = self.data['obs']
        data['obid'] = self.data['obid']
        return data

    class Meta:
        model = Marker
        fields = ('obid', 'obs')



class PrimerObSerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """
    class Meta:
        model = PrimerOb
        fields = ('obid', 'obs')

