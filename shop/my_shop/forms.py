from django.forms import ModelForm, TextInput, CheckboxInput, Textarea, SelectMultiple
from my_shop.models import Product, Categories, Invoices


class ProdForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'cid',
            'brand',
            'quantity',
            'desc',
            'images',
            'price',
            'old_price',
            'is_active',
        ]
        widgets = {"title":TextInput(attrs = {'class': 'form-control', 
                                                'style':"width:75%"}),
                    'cid':SelectMultiple(attrs={'class':'form-control'}),
                    'price':TextInput(attrs = {'class': 'form-control',
                                                'style':"width:75%"}),
                    'old_price':TextInput(attrs = {'class': 'form-control',
                                                'style':"width:75%"}),
                    'brand':TextInput(attrs = {'class': 'form-control',
                                                'style':"width:75%"}),
                    'quantity':TextInput(attrs = {'class': 'form-control',
                                                'style':"width:75%"}),
                    'images':TextInput(attrs = {'class': 'form-control',
                                                'style':"width:75%"}),
                    'is_active':CheckboxInput(attrs={'class':''}),
                    'desc':Textarea(attrs={'class':'form-control',
                                                'style':"width:75%"})
        }


class CatForm(ModelForm):
    class Meta:
        model = Categories
        fields = ['name']
        widgets = {"name":TextInput(attrs = {'class': 'form-control', 
                                                'style':"width:75%"}),       
        }

class InvoicesForm(ModelForm):
    class Meta:
        model = Invoices
        fields = ['note']

