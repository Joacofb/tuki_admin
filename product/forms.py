from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_type', 'product_description', 'product_supplier', 'product_sku',
                  'product_currency', 'product_price']
        labels = {
            'product_name': 'Nombre',
            'product_description': 'Detalles',
            'product_supplier': 'Proveedor',
            'product_sku': 'Codigo',
            'product_type': 'Tipo',
            'product_currency': 'Moneda',
            'product_price': 'Precio de lista',
        }
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Silenciador Delantero'}),
            'product_description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px;',
                                                         'placeholder': 'Silenciador ccorto con virola'}),
            'product_supplier': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Seleccione un proveedor'}),
            'product_sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'G04432'}),
            'product_type': forms.Select(attrs={'class': 'form-select'}),
            'product_currency': forms.TextInput(attrs={'class': 'form-control'}),
            'product_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
