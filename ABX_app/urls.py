from django.contrib import admin
from django.urls import path
from ABX_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('main_page/', views.main_page, name='main_page'),
    path('offers/', views.offers, name='offers'),
    path('new_offer/', views.new_offer, name='new_offer'),
    path('products/', views.products, name='products'),
    path('get_product/<int:product_id>/', views.get_product, name='get_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
]
