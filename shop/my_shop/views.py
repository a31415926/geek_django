from django.shortcuts import render, redirect, get_object_or_404
from my_shop.models import Product
from my_shop.forms import ProdForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.core import serializers


def main_page(request):
    products_all = Product.objects.all()
    paginator = Paginator(products_all, 6)
    page_num = request.GET.get('page', 1)
    products = paginator.get_page(page_num)
    return render(request, 'my_shop/main.html', context={'products':products.object_list, 'paginator':products})

def create_page(request):
    if request.method == 'POST':
        form_post = ProdForm(request.POST)
        if form_post.is_valid():
            new_obj = form_post.save()
            return redirect('post_detail', pid=new_obj.id)

    form = ProdForm()

    return render(request, 'my_shop/create.html', context={'forms': form})

def details_page(request, pid):
    goods_info = get_object_or_404(Product, id=pid)

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
            print(form)
            if not request.session.get('basket'):
                request.session['basket'] = {}
            goods_info = get_object_or_404(Product, id=pid)
            request.session['basket'][str(pid)] = {'qty' : int(form.get('add2basket')), 
                                                    'price':goods_info.price,
                                                    'title':goods_info.title,
                                                    }
            print(request.session['basket'])

    if not request.session.get('basket'):
        request.session['basket'] = {}
    
    goods_info = get_object_or_404(Product, id=pid)
    return render(request, 'my_shop/goods.html', context={'goods_info':goods_info})

def update_page(request, pid):

    if request.method == 'POST':
        form_post = ProdForm(request.POST)
        if form_post.is_valid():
            new_obj = form_post.save()
            return redirect('post_detail', pid=new_obj.id)

    obj = get_object_or_404(Product, id=pid)
    bound_form = ProdForm(instance=obj)
    return render(request, 'my_shop/update.html', context={'form':bound_form})


def search_page(request):
    search_val = request.GET.get('q')
    products = ''
    if search_val:
        products = Product.objects.filter(Q(title__icontains=search_val) | Q(description__icontains=search_val))
    return render(request, 'my_shop/search.html', context={'products':products})


def basket_page(request):
    if request.method == 'POST':
        form_post = request.POST
        print(form_post)
        if form_post.get('edit_qty'):
            request.session['basket'][form_post.get('pid')]['qty'] = int(form_post.get('edit_qty'))
            print(request.session['basket'])
        elif form_post.get('del'):
            del request.session['basket'][form_post.get('del')]
        elif form_post.get('-'):
            goods_qty = Product.objects.get(id=int(form_post.get('-')))
            if request.session['basket'][form_post.get('-')]['qty'] > 1:
                request.session['basket'][form_post.get('-')]['qty'] -= 1
            
        elif form_post.get('+'):
            goods_qty = Product.objects.get(id=int(form_post.get('+')))
            if goods_qty.quantity - request.session['basket'][form_post.get('+')]['qty'] > 1:
                request.session['basket'][form_post.get('+')]['qty'] += 1
            
    if not request.session.get('basket'):
        request.session['basket'] = {}
    products = request.session['basket']
    print(request.session['basket'])

    return render(request, 'my_shop/basket.html', context={'products':products})