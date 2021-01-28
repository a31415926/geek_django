import requests
import json
from time import sleep
from rozetka.models import Categories, Product


def get_all_ids_goods(id_cat):
    
    req = requests.get(f'https://xl-catalog-api.rozetka.com.ua/v3/goods/get?front-type=xl&category_id={id_cat}')
    temp_cat = requests.get(f'https://xl-catalog-api.rozetka.com.ua/v4/categories/getChildren?&category_id={id_cat}')
    cat_name = temp_cat.json()['data']['current']['title']
    temp_cat_full_path = temp_cat.json()['data']['current']['rz_mpath']
    temp_cat_full_path = temp_cat_full_path.split('.')
    cat_full_path = list(filter(None, temp_cat_full_path))
    cat_pid = temp_cat.json()['data']['current']['parent_id']
    cat_data = {
        'name':cat_name,
        'pid':cat_pid,
        'full_path':'|'.join(cat_full_path),
    }
    instance_cat = Categories.objects.get_or_create(cat_id=int(id_cat), defaults=cat_data)[0]
    if req.status_code == 200:
        all_request = req.json()
        ids_goods = all_request['data']['ids']
        get_goods_info(ids_goods, id_cat, instance_cat)
        total_pages_category = all_request['data']['total_pages']
        for id_page in range(2, total_pages_category+1):
            sleep(1)
            req_for_get_id_goods = requests.get(f'https://xl-catalog-api.rozetka.com.ua/v3/goods/get?front-type=xl&category_id={id_cat}&page={id_page}')
            if req_for_get_id_goods.status_code == 200:
                temp_ids_goods = req_for_get_id_goods.json()
                get_goods_info(temp_ids_goods, id_cat, instance_cat)
                ids_goods += temp_ids_goods['data']['ids']

    else:
        msg = 'Категория не найдена. Попробуй ввести другой ID'
        return msg
            

        
def get_goods_info(lst_ids, id_category, instance_cat):
    req_goods = requests.get(f'https://xl-catalog-api.rozetka.com.ua/v3/goods/getDetails?product_ids={lst_ids}')
    if req_goods.status_code == 200:
        all_goods = req_goods.json()
        all_goods = all_goods['data']
        good_info = {}
        for good in all_goods:
            #собираем нужную инфу про товар
            data_product = {
                'id_entry':good.get('id'),
                'title':good.get('title'),
                'brand':good.get('brand'),
                'desc':good.get('docket').replace('\n', '').replace('\r', ''),
                'link':good.get('href'),
                'images':'|'.join(good['images']['all_images']) if good.get('images') else '',
                'price':good.get('price'),
                'old_price':good.get('old_price'),
                'status':good.get('status'),
            }
            print(data_product['link'])
            inst_entry = Product.objects.get_or_create(id_entry=good.get('id'), defaults=data_product)[0]
            inst_entry.cid.add(instance_cat)
        
        return True


def scraper(id_category):
    get_all_ids_goods(id_category)
