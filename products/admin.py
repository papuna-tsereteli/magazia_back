from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Updated list_display and list_filter to use the new field
    list_display = ('image_preview', 'name', 'category', 'price', 'homepage_placement', 'popularity', 'date_added')
    list_filter = ('category', 'date_added', 'homepage_placement')
    search_fields = ('name', 'description')
    ordering = ('-popularity',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'სურათი'

