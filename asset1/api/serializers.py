from rest_framework import serializers
from asset1.models import Asset



class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'