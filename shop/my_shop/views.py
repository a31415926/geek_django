from django.shortcuts import render, redirect, get_object_or_404
from my_shop.models import Product, Basket
from my_shop.forms import ProdForm
from django.core.paginator import Paginator
from django.db.models import Q


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
    request.session.set_test_cookie()
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
            goods_info = get_object_or_404(Product, id=pid)
            data = {
                'title':goods_info.title,
                'price':goods_info.price,
                'qty':form.get('add2basket')            
            }
            Basket.objects.update_or_create(
                ssid = request.session.session_key,
                id_product = pid,
                defaults=data    
            )
            
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
    return render(request, 'my_shop/search.html', context={'products':products} )

def basket_page(request):
    products = Basket.objects.filter(ssid = request.session.session_key)
    if request.method == 'POST':
        form = request.POST
        if form.get('del'):
            Basket.objects.filter(
                ssid = request.session.session_key,
                id_product = form.get('del')
            ).delete()
        elif form.get('edit_qty'):
            goods_qty = Product.objects.get(id=int(form.get('pid'))).quantity
            basket_qty = Basket.objects.get(
                id_product=int(form.get('pid')),
                ssid = request.session.session_key,   
            )
            if basket_qty.qty < goods_qty:
                basket_qty.qty = form.get('edit_qty')
                basket_qty.save()

        elif form.get('-'):
            goods_qty = Product.objects.get(id=int(form.get('-')))
            basket_qty = Basket.objects.get(
                id_product=int(form.get('-')),
                ssid = request.session.session_key,   
            )
            if basket_qty.qty > 1:
                bk = Basket.objects.get(
                    id_product=int(form.get('-')),
                    ssid = request.session.session_key,   
                )
                bk.qty = bk.qty-1
                bk.save()

        elif form.get('+'):
            goods_qty = Product.objects.get(id=int(form.get('+'))).quantity
            basket_qty = Basket.objects.get(
                id_product=int(form.get('+')),
                ssid = request.session.session_key,   
            )
            if basket_qty.qty < goods_qty:
                basket_qty.qty = basket_qty.qty+1
                basket_qty.save()

    return render(request, 'my_shop/basket.html', context={'products':products})