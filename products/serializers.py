from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    # Add the new slider_image field to be included in the API response
    slider_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'image',
            'slider_image', # Add this line
            'category',
            'popularity',
            'created_at',
            'homepage_placement'
        ]

