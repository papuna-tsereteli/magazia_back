from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'description', 'image',
            'category', 'category_name', 'popularity', 'date_added',
            'homepage_placement' # Added the new field
        ]

