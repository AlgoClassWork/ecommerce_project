from django.contrib import admin

from shop.models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',) }

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created_at')
    list_editable = ('price', 'stock', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',) }

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'text', 'rating')
