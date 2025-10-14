from rest_framework import generics
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        # Updated filtering logic for homepage placement
        placement = self.request.query_params.get('placement')
        if placement:
            queryset = queryset.filter(homepage_placement=placement.upper())

        # Handle latest products filter
        latest = self.request.query_params.get('latest')
        if latest and latest.lower() == 'true':
            limit = int(self.request.query_params.get('limit', 4))  # Default limit to 4 if not specified
            return queryset.order_by('-date_added')[:limit]

        # Category filtering
        category_name = self.request.query_params.get('category')
        if category_name and category_name.lower() != 'all':
            queryset = queryset.filter(category__name__iexact=category_name)

        # Sorting
        sort_by = self.request.query_params.get('sortBy')
        if sort_by == 'price-asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price-desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'date-desc':
            queryset = queryset.order_by('-date_added')
        elif sort_by == 'date-asc':
            queryset = queryset.order_by('date_added')
        else:  # Default sort by popularity
            queryset = queryset.order_by('-popularity')

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

