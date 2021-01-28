from django.shortcuts import render
from rozetka.pars import scraper
from rozetka.models import Product, Categories
import re
from django.contrib import messages


# Create your views here.
def main_page(request):
    products_all = Categories.objects.filter(pid=0)
    return render(request, 'rozetka/main.html', context={'products':products_all})

def parser_goods(request):
    if request.method == 'POST':
        url = request.POST.get('value')
        if url:
            temp_result = re.findall(r'rozetka\.com\.ua/.*/\w(\d*)/?', url)
            if temp_result:
                messages.add_message(request, messages.INFO, 'start parsing')
                scraper(temp_result[0])
            else:
                messages.add_message(request, messages.INFO, 'Link error')
                print('no')

    #scraper('80066')
    return render(request, 'rozetka/parser.html')

def goods_of_cats(request, cat_id):
    products = Product.objects.filter(cid=cat_id)
    return render(request, 'rozetka/goods_of_cats.html', context={'products':products})
