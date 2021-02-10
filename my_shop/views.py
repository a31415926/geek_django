from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from my_shop.models import Product, Categories, Invoices
from my_shop.forms import ProdForm, CatForm, InvoicesForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.models import model_to_dict
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy
import json
import hashlib
from time import time


class HomePage(ListView):
    """ главная """
    model = Categories
    template_name = 'my_shop/main.html'
    context_object_name = 'products'


class CreateGoodsView(CreateView):
    """ создание товара """
    model = Product
    template_name = 'my_shop/create.html'
    form_class = ProdForm

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.id})


class CreateCategoryView(CreateView):
    """ создание категории """
    model = Categories
    template_name = 'my_shop/create.html'
    form_class = ProdForm
    success_url = reverse_lazy('main_page')


class DetailPageView(DetailView):
    """ temp """
    model = Product
    template_name = 'my_shop/goods.html'

    def get_queryset(self):
        return Product.objects.filter(id = self.kwargs['pk'])


def details_page(request, pk):
    goods_info = get_object_or_404(Product, id=pk)
    
    if request.method == 'POST':
        form = request.POST
        if form.get('activate'):
            post = Product.objects.get(id=form['activate'])
            post.is_active = True
            post.save()
        elif form.get('hide'):
            post = Product.objects.get(id=form['hide'])
            post.is_active = False
            post.save()
        elif form.get('delete'):
            post = Product.objects.get(id=form['delete']).delete()
            return redirect('main_page')
        elif form.get('add2basket'):
            if not request.session.get('basket'):
                request.session['basket'] = {}
            goods_info = model_to_dict(get_object_or_404(Product, id=pk))
            del goods_info['cid']
            request.session['basket'][str(pk)] = goods_info
            request.session['basket'][str(pk)]['qty'] = int(form.get('add2basket'))

            print(request.session['basket'])

    if not request.session.get('basket'):
        request.session['basket'] = {}
    
    goods_info = get_object_or_404(Product, id=pk)
    return render(request, 'my_shop/goods.html', context={'goods_info':goods_info})


class UpdateGoodsView(UpdateView):
    """ обновление товаров """
    model = Product
    template_name = 'my_shop/update.html'
    form_class = ProdForm

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})


class CategoryPage(ListView):
    """ страница с материалами категории """
    model = Product
    template_name = 'my_shop/cats.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(cid = self.kwargs['pk'])


class SearchPageView(ListView):
    """ страница поиска """
    model = Product
    template_name = 'my_shop/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        search_val = self.request.GET['q']
        context = Product.objects.filter(
                Q(title__icontains=search_val) | Q(desc__icontains=search_val)
            )
        return context


def basket_page(request):
    if request.method == 'POST':
        form_post = request.POST
        print(form_post)


        if form_post.get('action'):
            if form_post['action'] == 'edit_qty':
                good_id = form_post.get('id')
                request.session['basket'][good_id]['qty'] = int(form_post.get('qty'))
                data = request.session['basket'][good_id] 
                return HttpResponse(json.dumps(data), content_type='application/json')

            elif form_post['action'] == '-':
                good_id = form_post.get('id')
                goods_qty = Product.objects.get(id=int(good_id))
                if request.session['basket'][good_id]['qty'] > 1:
                    request.session['basket'][good_id]['qty'] -= 1
                    data = request.session['basket'][good_id] 
                    return HttpResponse(json.dumps(data), content_type='application/json')
                
            elif form_post['action'] == '+':
                good_id = form_post.get('id')
                goods_qty = Product.objects.get(id=int(good_id))
                if goods_qty.quantity - request.session['basket'][good_id]['qty'] > 1:
                    request.session['basket'][good_id]['qty'] += 1
                    data = request.session['basket'][good_id] 
                    return HttpResponse(json.dumps(data), content_type='application/json')
            
            elif form_post['action'] == 'del':
                good_id = form_post.get('id')
                del request.session['basket'][good_id]
                data = {'del':good_id}
                return HttpResponse(json.dumps(data), content_type='application/json')


            
    if not request.session.get('basket'):
        request.session['basket'] = {}
    products = request.session['basket']
    print(request.session['basket'])

    return render(request, 'my_shop/basket.html', context={'products':products})



class CheckoutPage(CreateView):
    """ страница оформления заказа """
    model = Invoices
    form_class = InvoicesForm
    template_name = 'my_shop/checkout.html'

    def get_context_data(self, **kwargs):
        if not self.request.session.get('basket'):
            self.request.session['basket'] = {}
        products = self.request.session['basket']
        temp_cost = self.request.session['basket'].values()
        total_cost = 0
        for i in temp_cost:
            total_cost+=int(i['qty'])*i['price']
        context = super().get_context_data(**kwargs)
        context['products'] = products
        context['total_cost'] = total_cost
        return context

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.goods = self.request.session['basket']
        self.object.slug = hashlib.sha512((str(time()) + str(self.object.id) ).encode('utf-8')).hexdigest()
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('invoice_page', kwargs={'slug': self.object.slug})

class InvoicesPageView(DetailView):
    model = Invoices
    template_name = 'my_shop/invoice.html'
    context_object_name = 'invoice'

    def get_queryset(self):
        print(self.kwargs['slug'])
        return Invoices.objects.filter(slug = self.kwargs['slug'])

