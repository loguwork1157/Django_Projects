from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price', 'description']

# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=150)
#     quantity = forms.IntegerField(min_value=0)
#     price = forms.DecimalField(max_digits=8, decimal_places=2)
#     description = forms.CharField(widget=forms.Textarea, required=False)
#     expiry = forms.DateField(required=False, widget=forms.SelectDateWidget)