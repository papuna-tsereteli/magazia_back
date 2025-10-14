from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        category_name = self.request.query_params.get('category', None)
        if category_name and category_name.lower() != 'all':
            queryset = queryset.filter(category__name__iexact=category_name)

        sortBy = self.request.query_params.get('sortBy', 'date-desc')  # Default sort
        if sortBy == 'price-asc':
            queryset = queryset.order_by('price')
        elif sortBy == 'price-desc':
            queryset = queryset.order_by('-price')
        elif sortBy == 'popularity':
            queryset = queryset.order_by('-popularity')
        else:  # Default sort by date
            queryset = queryset.order_by('-created_at')

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# NEW: A dedicated view for all homepage data
class HomepageDataView(APIView):
    def get(self, request, format=None):
        # Query for products set to 'SLIDER'
        slider_products_qs = Product.objects.filter(homepage_placement='SLIDER').order_by('-popularity')

        # Query for products set to 'FEATURED', limit to 8
        featured_products_qs = Product.objects.filter(homepage_placement='FEATURED').order_by('-popularity')[:8]

        # Query for the latest 8 products overall
        latest_products_qs = Product.objects.order_by('-created_at')[:8]

        # Pass context to serializers to build absolute image URLs
        context = {'request': request}
        slider_serializer = ProductSerializer(slider_products_qs, many=True, context=context)
        featured_serializer = ProductSerializer(featured_products_qs, many=True, context=context)
        latest_serializer = ProductSerializer(latest_products_qs, many=True, context=context)

        return Response({
            'slider_products': slider_serializer.data,
            'featured_products': featured_serializer.data,
            'latest_products': latest_serializer.data,
        })