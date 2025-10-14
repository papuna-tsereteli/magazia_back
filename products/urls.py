from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryListView

urlpatterns = [
    # Existing paths
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    # New path for categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
]

