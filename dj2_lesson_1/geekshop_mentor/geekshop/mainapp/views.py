from basketapp.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import datetime
import random
from .models import ProductCategory, Product
from django.shortcuts import get_object_or_404



# **************************************************************************************

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user = user)
    else:
        return []


def get_hot_product():
    products = Product.objects.filter(category__is_active=True)
    
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category = hot_product.category). \
                        exclude(pk = hot_product.pk)[:3]
    
    return same_products

# ***********************************************************************************************

def main(request):
    title = 'главная'
    
    products = Product.objects.all()[:4]
    
    content = {
        'title': title,
        'products': products,
        # 'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', content)

# *******************************************************************************************


def products(request, pk=None, page= 1):
  
    basket = get_basket(request.user)
    title = 'продукты'
    links_menu = ProductCategory.objects.all()
    
    content = {
        'title'     : title,
        'links_menu': links_menu,
        # 'basket'    : basket,
    }

    if pk is not None:
        if pk == 0:
            products = Product.objects.filter(is_active=True).order_by('price')
            category = {pk:0, 'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk = pk)
            products = Product.objects.filter(category__pk = pk, is_active=True).order_by('price')



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
    title = 'о нас'
    visit_date = datetime.datetime.now()
    locations = [
        {
            'city': 'Москва',
            'phone': '+7-888-888-8888',
            'email': 'info@geekshop.ru',
            'address': 'В пределах МКАД',
        },
        {
            'city': 'Екатеринбург',
            'phone': '+7-777-777-7777',
            'email': 'info_yekaterinburg@geekshop.ru',
            'address': 'Близко к центру',
        },
        {
            'city': 'Владивосток',
            'phone': '+7-999-999-9999',
            'email': 'info_vladivostok@geekshop.ru',
            'address': 'Близко к океану',
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
    title = 'продукты'
    
    content = {
        'title'     : title,
        'links_menu': ProductCategory.objects.all(),
        'product'   : get_object_or_404(Product, pk = pk),
        # 'basket'    : get_basket(request.user),
    }
    
    return render(request, 'mainapp/product.html', content)



    
    
