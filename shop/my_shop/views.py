from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from my_shop.models import Product, Categories
from my_shop.forms import ProdForm, CatForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.models import model_to_dict
import json


def main_page(request):
    products_all = Categories.objects.all()
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

def create_cats(request):
    if request.method == 'POST':
        form_post = CatForm(request.POST)
        if form_post.is_valid():
            new_obj = form_post.save()
            return redirect('main_page')

    form = CatForm()

    return render(request, 'my_shop/create_cat.html', context={'forms': form})

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
            if not request.session.get('basket'):
                request.session['basket'] = {}
            goods_info = model_to_dict(get_object_or_404(Product, id=pid))
            del goods_info['cid']
            request.session['basket'][str(pid)] = goods_info
            request.session['basket'][str(pid)]['qty'] = int(form.get('add2basket'))

            print(request.session['basket'])

    if not request.session.get('basket'):
        request.session['basket'] = {}
    
    goods_info = get_object_or_404(Product, id=pid)
    return render(request, 'my_shop/goods.html', context={'goods_info':goods_info})

def update_page(request, pid):

    if request.method == 'POST':
        obj = Product.objects.get(id=pid)
        form_post = ProdForm(request.POST, instance=obj)
        if form_post.is_valid():
            new_obj = form_post.save()
            return redirect('post_detail', pid=new_obj.id)

    obj = get_object_or_404(Product, id=pid)
    bound_form = ProdForm(instance=obj)
    return render(request, 'my_shop/update.html', context={'form':bound_form})

def cats_page(request, pid):
    products_all = Product.objects.all()
    paginator = Paginator(products_all, 6)
    page_num = request.GET.get('page', 1)
    products = paginator.get_page(page_num)
    return render(request, 'my_shop/cats.html', context={'products':products.object_list, 'paginator':products})


def search_page(request):
    search_val = request.GET.get('q')
    products = ''
    if search_val:
        products = Product.objects.filter(Q(title__icontains=search_val) | Q(desc__icontains=search_val))
    return render(request, 'my_shop/search.html', context={'products':products})


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


def checkout_page(request):
     
    if not request.session.get('basket'):
        request.session['basket'] = {}
    products = request.session['basket']
    temp_cost = request.session['basket'].values()
    total_cost = 0
    for i in temp_cost:
        total_cost+=int(i['qty'])*i['price']
    

    return render(request, 'my_shop/checkout.html', context={'products':products, 'total_cost':total_cost})


