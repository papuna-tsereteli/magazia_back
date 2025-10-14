from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Updated list_display to include a thumbnail for the slider image
    list_display = ('name', 'format_image_thumbnail', 'format_slider_image_thumbnail', 'category', 'price', 'popularity', 'homepage_placement')
    list_filter = ('category', 'homepage_placement', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    list_editable = ('price', 'popularity', 'homepage_placement')

    # Group fields into logical sections
    fieldsets = (
        ("ძირითადი ინფორმაცია", {
            "fields": ("name", "description", "category")
        }),
        ("სურათები", {
            "fields": ("image", "slider_image")
        }),
        ("ფასი და ჩვენება", {
            "fields": ("price", "popularity", "homepage_placement")
        }),
    )

    def format_image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "სურათი არ არის"
    format_image_thumbnail.short_description = "პროდუქტის სურათი"

    # New method to display slider image thumbnail in the list
    def format_slider_image_thumbnail(self, obj):
        if obj.slider_image:
            return format_html('<img src="{}" width="100" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.slider_image.url)
        return "სურათი არ არის"
    format_slider_image_thumbnail.short_description = "სლაიდერის სურათი"

