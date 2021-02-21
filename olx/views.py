from django.shortcuts import render
import subprocess
from olx.models import ScrapeTask

def parse_page(requests):

    if requests.method == 'POST':
        link_cat = requests.POST.get('link')
        qty = requests.POST.get('qty')
        if int(qty)>0:
            sub_id = ScrapeTask.objects.create(
                link = link_cat, 
                qty=qty,
            )
            sub = subprocess.Popen(['python', 'parse_olx.py', link_cat, qty, str(sub_id.pk)], shell=True)

    return render(requests, 'olx/parse.html')
# Create your views here.
