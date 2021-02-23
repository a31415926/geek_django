from django.shortcuts import render
import subprocess
from olx.models import ScrapeTask
from multiprocessing import Process
from olx import parser

def parse_page(requests):

    if requests.method == 'POST':
        link_cat = requests.POST.get('link')
        qty = requests.POST.get('qty')
        if int(qty)>0:
            proccess_parse = Process(target=parser.main, args=(link_cat, qty))
            proccess_parse.start()
            """sub_id = ScrapeTask.objects.create(
                link = link_cat, 
                qty=qty,
            )
            sub = subprocess.Popen(['python', 'parse_olx.py', link_cat, qty, str(sub_id.pk)], shell=True)"""

    return render(requests, 'olx/parse.html')