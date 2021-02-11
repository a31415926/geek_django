from rest_framework import serializers
from my_shop.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name']