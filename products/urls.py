from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    CategoryListView,
    HomepageDataView  # Import the new view
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),

    # NEW: The single endpoint for all homepage data
    path('homepage-data/', HomepageDataView.as_view(), name='homepage-data'),
]