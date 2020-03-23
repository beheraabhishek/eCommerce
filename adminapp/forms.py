from django import forms
from .models import MerchantModel, ProductModel


class MerchantForm(forms.ModelForm):
    class Meta:
        model = MerchantModel
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = '__all__'
