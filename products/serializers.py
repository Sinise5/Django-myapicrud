from rest_framework import serializers
from .models import Product  # Pastikan model ini ada

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
