import adminapp.views as adminapp
from django.urls import path, re_path

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', adminapp.user_create, name='user_create'),
    # path('users/read/', adminapp.users, name='users'),    # for Function Base Vieus
    path('users/read/', adminapp.UsersListView.as_view(), name='users'),    # for CBV
    path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),

    # path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', adminapp.categories, name='categories'),
    # path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    # path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    # re_path('categories/delete/(?P<pk>[0-9]+)/$', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),
    path('categories/delete/<int:pk>', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),
    # categories/delete/(?P<pk>[0-9]+)/$
    # categories/delete/<int:pk>/

    path('products/create/category/<int:pk>/', adminapp.product_create, name='product_create'),
    # path('products/read/<int:pk>/', adminapp.product_read, name='product_read'),
    path('products/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),
    path('products/read/category/<int:pk>/', adminapp.products, name='products'),
    path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('products/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
    
]
