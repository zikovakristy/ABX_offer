from django.contrib import admin
from .models import Product, Region, RegionGroup

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_code', 'sale_price', 'purchase_price', 'default', 'product_type', 'HS', 'AS', 'RC', 'PC', 'sleva', 'DPH', 'price_with_DPH')

admin.site.register(Region)
admin.site.register(RegionGroup)
