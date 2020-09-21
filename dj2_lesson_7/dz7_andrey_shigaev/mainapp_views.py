from basketapp.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import datetime
import random
from .models import ProductCategory, Product
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page


def get_links_menu():
   if settings.LOW_CACHE:
       key = 'links_menu'
       links_menu = cache.get(key)
       if links_menu is None:
           links_menu = ProductCategory.objects.filter(is_active=True)
           cache.set(key, links_menu)
       return links_menu
   else:
       return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
       key = f'category_{pk}'
       category = cache.get(key)
        if category is None:
           category = get_object_or_404(ProductCategory, pk=pk)
           cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
   if settings.LOW_CACHE:
       key = 'products'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
   if settings.LOW_CACHE:
       key = f'product_{pk}'
       product = cache.get(key)
       if product is None:
           product = get_object_or_404(Product, pk=pk)
           cache.set(key, product)
       return product
   else:
       return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
   if settings.LOW_CACHE:
       key = 'products_orederd_by_price'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
   if settings.LOW_CACHE:
       key = f'products_in_category_orederd_by_price_{pk}'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


##########################################################################################



def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user = user)
    else:
        return []


def get_hot_product():
    # products = Product.objects.filter(category__is_active=True)    # memcached
    products = get_products()                                        # memcached
    
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    # same_products = Product.objects.filter(category = hot_product.category).exclude(pk = hot_product.pk)[:3]  # memcached
    products = get_products()[:3]                           # memcached
    
    return same_products

# ***********************************************************************************************

def main(request):
    title = '�������'
	products = get_products()[:3]		# memcached
    
    # products = Product.objects.all()[:4]
    # products = Product.objects.filter(is_active=True, category__is_active=True)[:4]
    # products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:4]

    
    content = {
        'title': title,
        'products': products,
        # 'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', content)

# *******************************************************************************************

@cache_page(3600)
def products(request, pk=None, page= 1):
  
    basket = get_basket(request.user)
    title = '��������'
    links_menu = ProductCategory.objects.all()
    
    content = {
        'title'     : title,
        'links_menu': links_menu,
        # 'basket'    : basket,
    }

    if pk is not None:
        if pk == 0:
            # products = Product.objects.filter(is_active=True).order_by('price')   # memcached
            products = get_products_orederd_by_price()      # memcached
            category = {pk:0, 'name': '���'}
        else:
            # category = get_object_or_404(ProductCategory, pk = pk)    # memcached
            category = get_category(pk) # memcached

            # products = Product.objects.filter(category__pk = pk, is_active=True).order_by('price')    # memcached
            products = get_products_in_category_orederd_by_price(pk)    # memcached


    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)




# ***************************** pagination ********************************************

     
        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

      
            
        content['category'] = category
        # content['products'] = products
        content['products'] = products_paginator
        
        
    
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)


    content['same_products'] = same_products
    content['hot_product'] = hot_product
    return render(request, 'mainapp/products.html', content)
    


def contact(request):
    title = '� ���'
    if settings.LOW_CACHE:
    key = f'locations'
    locations = cache.get(key)
        if locations is None:
           locations = load_from_json('contact__locations')
           cache.set(key, locations)
    else:
       locations = load_from_json('contact__locations')

    visit_date = datetime.datetime.now()
    locations = [
        {
            'city': '������',
            'phone': '+7-888-888-8888',
            'email': 'info@geekshop.ru',
            'address': '� �������� ����',
        },
        {
            'city': '������������',
            'phone': '+7-777-777-7777',
            'email': 'info_yekaterinburg@geekshop.ru',
            'address': '������ � ������',
        },
        {
            'city': '�����������',
            'phone': '+7-999-999-9999',
            'email': 'info_vladivostok@geekshop.ru',
            'address': '������ � ������',
        },
    ]
    content = {
        'title': title,
        'visit_date':visit_date,
        'locations': locations,
        # 'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/contact.html', content)


def product(request, pk):
    title = '��������'
    links_menu = get_links_menu()
    product = get_product(pk)

    
    content = {
        'title'     : title,
        'links_menu': ProductCategory.objects.all(),

        'product'   : get_object_or_404(Product, pk = pk),

        # 'basket'    : get_basket(request.user),
    }
    
    return render(request, 'mainapp/product.html', content)