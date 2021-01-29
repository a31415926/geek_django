from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200, default='No name', db_index=True)
    price = models.FloatField(default=0.0)
    description = models.TextField(blank=True, default='', db_index=True)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    class Meta:
        ordering = ['-date_add']


class Basket(models.Model):
    id_product = models.IntegerField(default=1)
    title = models.CharField(max_length=200, default='Empty')
    qty = models.IntegerField(default=1)
    price = models.FloatField(default=0)
    date_add = models.DateTimeField(auto_now_add=True)
    ssid = models.CharField(max_length=150, default='empty')

    def __str__(self):
        return self.ssid