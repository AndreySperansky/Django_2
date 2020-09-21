from django.urls import path
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),   # все товары
    path('category/<int:pk>/', cache_page(3600)(mainapp.products), name='category'),  
    path('category/<int:pk>/page/<int:page>/', mainapp.product, name='page'),  
    path('product/<int:pk>/', mainapp.product, name='product'),  
]
