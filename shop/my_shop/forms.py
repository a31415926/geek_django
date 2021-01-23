from django.forms import ModelForm, TextInput, CheckboxInput, Textarea
from my_shop.models import Product


class ProdForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'quantity', 'is_active']
        widgets = {"title":TextInput(attrs = {'class': 'form-control', 
                                                'style':"width:75%"}),
                    'price':TextInput(attrs = {'class': 'form-control',
                                                'style':"width:75%"}),
                    'quantity':TextInput(attrs = {'class': 'form-control',
                                                'style':"width:75%"}),
                    'is_active':CheckboxInput(attrs={'class':'form-check-input'}),
                    'description':Textarea(attrs={'class':'form-control',
                                                'style':"width:75%"})
        
        }

