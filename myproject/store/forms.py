from django import forms
from .models import Product, Shipment, Transaction, LineItem

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

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['shipping_provider', 'line_item', 'status']
        widgets = {
            'shipping_provider': forms.TextInput(attrs={'class': 'form-control'}),
            'line_item': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show all line items with custom labels
        self.fields['line_item'].queryset = LineItem.objects.all()
        self.fields['line_item'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return f"LineItem #{obj.id} - Transaction #{obj.transaction.transaction_id} - {obj.product_name}"