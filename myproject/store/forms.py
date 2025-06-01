from django import forms
from .models import Product

# Ensure the Product model has the fields: name, price, stock, description, and image.

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'description', 'image']
        widgets = {
            'name' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product price'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product stock'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 4
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'placeholder': 'Upload product image'
            })
        }
        help_texts = {
            'name': 'Enter the name of the product.',
            'price': 'Enter the price of the product.',
            'stock': 'Enter the available stock for the product.',
            'description': 'Provide a detailed description of the product.',
            'image': 'Upload an image of the product.'
        }
        error_messages = {
            'name': {
                'required': 'Product name is required.',
                'max_length': 'Product name cannot exceed 100 characters.'
            },
            'price': {
                'required': 'Product price is required.',
                'invalid': 'Enter a valid price.'
            },
            'stock': {
                'required': 'Stock quantity is required.',
                'invalid': 'Enter a valid stock quantity.'
            }
        }
        labels = {
            'name': 'Product Name',
            'price': 'Price',
            'stock': 'Stock Quantity',
            'description': 'Description',
            'image': 'Product Image'
        }