import django
django.setup()
import requests
from bs4 import BeautifulSoup
import csv
import os 
import time
import sys
import re
import random
import urllib3
from olx import models



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



"""
Берутся только обычные объявления, топовые рекламные пропускаем
скрипт парсит все объявления категории (с учетом пагинации)
"""


def parse_board(link_cat, cnt=0, temp_cnt = 0):
    count_entry = temp_cnt
    session = requests.Session()
    req_cat = session.get(link_cat, verify=False)
    entry_soap = BeautifulSoup(req_cat.text, 'lxml')
    all_entries = entry_soap.select('#offers_table.fixed.offers.breakword.redesigned .marginright5.link.linkWithHash.detailsLink')
    for link_entry in all_entries:
        time.sleep(random.uniform(1, 2))
        req_entry = session.get(link_entry.get('href'), verify=False)
        entry_info = BeautifulSoup(req_entry.text, 'lxml')
        entry_category = entry_info.select_one('.inline:last-child .link.nowrap span') #категория материала
        entry_category = entry_category.text if entry_category else ''
        price = entry_info.select_one('.pricelabel .pricelabel__value')
        price = price.text if price else ''
        author_name = entry_info.select_one('.offer-user__actions h4 a')
        author_name = author_name.text.strip() if author_name else 'not found'
        author_phone = ''
        entry_date = entry_info.select_one('.offer-bottombar__item>em>strong')
        entry_date = entry_date.text if entry_date else ''
        entry_id = entry_info.select_one('div.clm-samurai')
        entry_id = entry_id.get('data-item') if entry_id else ''
        link_author = entry_info.select_one('a#linkUserAds')
        link_author = link_author.get('href') if link_author else ''
        entry_title = entry_info.select_one('.offer-titlebox h1')
        entry_title = entry_title.text.strip() if entry_title else 'not found'
        is_phone = entry_info.select_one('.contact-button.link-phone')

        if is_phone:
            token_id_re = re.findall(r"-ID(.*?).html", link_entry.get('href'))
            token_id = token_id_re[0]
            token = entry_info.select_one('.offer-section>script')
            token_res = re.findall(r"var phoneToken = '(.*?)';", str(token))
            headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36', 'referer':link_entry.get('href')}
            req_phone = session.get('https://www.olx.ua/ajax/misc/contact/phone/'+token_id+'/?pt='+token_res[0], headers = headers)
            
            #если попали под 403, ждем немного и идем дальше
            if req_phone.status_code == 403:
                time.sleep(100)
                req_phone = session.get('https://www.olx.ua/ajax/misc/contact/phone/'+token_id+'/?pt='+token_res[0], headers = headers)
            
            req_phone_json = req_phone.json()
            author_phone = req_phone_json['value']
            
            #может быть указан не один номер телефона, учитываем это.
            if 'span' in author_phone:
                phone_soup = BeautifulSoup(author_phone, 'lxml')
                temp_phone = phone_soup.select('.block')
                temp_phones = []
                for row in temp_phone:
                    temp_phones.append(row.text)

                author_phone = ', '.join(temp_phones)
        
        models.OlxProduct.objects.get_or_create(id_olx = entry_id,
            defaults={
                'title':entry_title,
                'category' : entry_category,
                'price' : price,
                'author_name' : author_name,
                'phone' : author_phone,
                'entry_date' : entry_date,
                'author_link' : link_author,
                'link_entry' : link_entry.get('href'),
            }
        )
        print(link_entry.get('href'))
        count_entry += 1
        if count_entry == cnt:
            print('the end')
            """models.ScrapeTask.objects.filter(
                pk=int(sys.argv[3])
            ).update(notes='success', state=True)"""
            return

      
    
    next_page = entry_soap.select_one('.fbold.next.abs.large a.link.pageNextPrev')
    if next_page:
        time.sleep(3)
        parse_board(next_page.get('href'), temp_cnt=count_entry)


#if __name__ == '__main__':
def main(link, qty):
    if 'olx.ua' in link and requests.get(link).status_code == 200:
        parse_board(link, cnt=int(qty))
    