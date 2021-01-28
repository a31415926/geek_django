from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=300, default='Noname')
    id_entry = models.IntegerField(unique=True, primary_key=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    desc = models.TextField(blank=True)
    link = models.CharField(max_length=200)
    images = models.CharField(blank=True, max_length=700)
    price = models.FloatField()
    old_price = models.FloatField(blank=True)
    status = models.CharField(blank=True, max_length=100)
    cid = models.ManyToManyField('Categories')

    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=250, default='Noname cat')
    cat_id = models.IntegerField(unique=True, primary_key=True)
    pid = models.IntegerField(default=0)
    full_path = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.name