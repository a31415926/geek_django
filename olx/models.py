from django.db import models


class OlxProduct(models.Model):

    id_olx = models.IntegerField(unique=True)
    link_entry = models.CharField(default='', blank=True, null=True, max_length=200)
    title = models.CharField(default='', blank=True, null=True, max_length=200)
    category = models.CharField(default='', blank=True, null=True, max_length=200)
    price = models.CharField(default='', null=True, max_length=100)
    author_name = models.CharField(default='', blank=True, null=True, max_length=150)
    phone = models.CharField(default='', blank=True, null=True, max_length=150)
    entry_date = models.CharField(default='', null=True, max_length=150)
    author_link = models.CharField(default='', null=True, blank=True, max_length=150)



class ScrapeTask(models.Model):
    link = models.CharField(default='', blank=True, null=True, max_length=150)
    qty = models.IntegerField(blank=True, null=True)
    state = models.BooleanField(default=False)
    add_date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=150, blank=True, null=True, default='')