from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=300, default='Noname')
    quantity = models.IntegerField(blank=True, default=10) #default 10 for tests
    id_rozetka = models.IntegerField(blank=True, default=0)
    brand = models.CharField(max_length=100, blank=True, null=True)
    desc = models.TextField(blank=True, default='')
    images = models.CharField(blank=True, max_length=700, default='')
    price = models.FloatField(default=0)
    old_price = models.FloatField(blank=True, default=0)
    is_active = models.BooleanField(blank=False, max_length=100)
    cid = models.ManyToManyField('Categories')
    date_add = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_add']


class Categories(models.Model):
    name = models.CharField(max_length=250, default='Noname cat', unique=True)
    id_rozetka = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name