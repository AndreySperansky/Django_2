from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm
from django.contrib.auth.decorators import user_passes_test
from adminapp.forms import ProductEditForm
# *************************** Class Based Vies ****************************************
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import DetailView







# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     content = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', content)

# CBV  *****************************************************************************

class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['title'] = 'пользователи/список'
        return context
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(is_active = True)
    
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)




@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'
    
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()
    
    content = {'title': title, 'update_form': user_form}
    
    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'
    
    edit_user = get_object_or_404(ShopUser, pk = pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance = edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update', args = [edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance = edit_user)
    
    content = {'title': title, 'update_form': edit_form}
    
    return render(request, 'adminapp/user_update.html', content)




@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'
    
    user = get_object_or_404(ShopUser, pk = pk)
    
    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        # user.is_active = False
        # user.save()
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))
    
    content = {'title': title, 'user_to_delete': user}
    
    return render(request, 'adminapp/user_delete.html', content)


'''
*****************************************************************************************************
                                        CATEGORIES
*****************************************************************************************************
'''


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all().order_by('-is_active', '-id')

    content = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', content)




# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#
#     if request.method == 'POST':
#         user_form = ProductCategoryEditForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         user_form = ProductCategoryEditForm()
#
#     content = {'title': title, 'update_form': user_form}
#
#     return render(request, 'adminapp/category_update.html', content)


# CBV  **********************************************************************************

class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm    # taken from the forms.py
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    # fields = '__all__'                    # if not to bring up 'form class = ProductCategoryEditForm'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
    
        return context

#  end CBV ********************************************************************************



# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#
#     category = get_object_or_404(ProductCategory, pk = pk)
#
#     if request.method == 'POST':
#         update_form = ProductCategoryEditForm(request.POST, request.FILES, instance = category)
#         if update_form.is_valid():
#             update_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         update_form = ProductCategoryEditForm(instance = category)
#
#     content = {'title': title, 'update_form': update_form}
#
#     return render(request, 'adminapp/category_update.html', content)

# CBV  **********************************************************************************

class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        
        return context
    
    
#  end CBV ********************************************************************************


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'категории/удаление'

    category = get_object_or_404(ProductCategory, pk = pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        # user.is_active = False
        # user.save()
        if category.is_active:
            category.is_active = False
        else:
            category.is_active = True
        category.save()
        return HttpResponseRedirect(reverse('admin:categories'))

    content = {'title': title, 'category_to_delete': category}

    return render(request, 'adminapp/category_delete.html', content)

# CBV  **********************************************************************************
#


# class ProductCategoryDeleteView(DeleteView):
#     model = ProductCategory
#     template_name = 'adminapp/category_delete.html'
#     success_url = reverse_lazy('admin:categories')
#
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         self.object.is_active = False
#         self.object.save()
#
#         return HttpResponseRedirect(self.get_success_url())  #  redirect to var success_url
#
#     # def delete(self, request, *args, **kwargs):
#     #     if self.object.is_active:
#     #       self.object.is_active = False
#     #     else:
#     #       self.object.is_active = True
#     #     self.object.save()
#     #
#     #     return HttpResponseRedirect(self.get_success_url())  #  redirect to var success_url
#
#

    
#  end CBV ********************************************************************************



'''
*******************************************************************************************
PRODUCT
*******************************************************************************************
'''


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')
    # products_list = Product.objects.filter(category=category).order_by('-id')

    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', content)



# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk = pk)
#     content = {
#         'title': title,
#         'object': product,
#     }
#     return render(request, 'adminapp/product_read.html', content)


# CBV  **********************************************************************************

class ProductDetailView(DetailView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')
    
    
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
   
#  end CBV ********************************************************************************



@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукт/создание'
    category = get_object_or_404(ProductCategory, pk = pk)
    
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args = [pk]))
    else:
        product_form = ProductEditForm(initial = {'category': category})
    
    content = {'title'      : title,
               'update_form': product_form,
               'category'   : category
               }
    
    return render(request, 'adminapp/product_update.html', content)



@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'
    
    edit_product = get_object_or_404(Product, pk = pk)
    
    if request.method == 'POST':
        # request.POST, request.FILES, - то что ввел пользователь
        # instance = edit_product - объект который будем изменять
        edit_form = ProductEditForm(request.POST, request.FILES, instance = edit_product)
        if edit_form.is_valid():
            edit_form.save()
            # args = [edit_product.pk] - товар который редактируем
            return HttpResponseRedirect(reverse('admin:product_update', args = [edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance = edit_product)
    
    content = {'title'      : title,
               'update_form': edit_form,
               'category'   : edit_product.category
               }
    
    return render(request, 'adminapp/product_update.html', content)



@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'
    
    product = get_object_or_404(Product, pk = pk)

    if request.method == 'POST':
        if product.is_active:
            product.is_active = False
        else:
            product.is_active = True
        product.save()
        return HttpResponseRedirect(reverse('admin:products', args = [product.category.pk]))
        # return HttpResponseRedirect(reverse('admin:products', args = [product.category_id]))
    
    content = {
        'title': title,
        'product_to_delete': product
    }
    
    return render(request, 'adminapp/product_delete.html', content)




