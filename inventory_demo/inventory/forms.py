from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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


class SignupForm(UserCreationForm):
    """Extend UserCreationForm with an email field."""
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user