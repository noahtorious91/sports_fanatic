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
    transaction = forms.ModelChoiceField(
        queryset=Transaction.objects.all(),
        empty_label="Select a transaction...",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_transaction'}),
        help_text="Select a transaction to see its line items",
        required=False  # Make it optional since it's not saved to the model
    )
    
    line_items = forms.ModelMultipleChoiceField(
        queryset=LineItem.objects.none(),  # Initially empty
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select line items from the chosen transaction"
    )

    class Meta:
        model = Shipment
        fields = ['shipping_provider', 'status']  # Remove 'transaction' from here
        widgets = {
            'shipping_provider': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter shipping provider (e.g., FedEx, UPS, DHL)'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Custom label for transactions
        self.fields['transaction'].label_from_instance = lambda obj: f"Transaction #{obj.transaction_id} - {obj.user.username} ({obj.created_at.strftime('%m/%d/%Y')})"
        
        # If transaction is selected, show its line items
        if 'transaction' in self.data:
            try:
                transaction_id = int(self.data.get('transaction'))
                self.fields['line_items'].queryset = LineItem.objects.filter(transaction_id=transaction_id)
                self.fields['line_items'].label_from_instance = self.label_from_instance
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # For editing existing shipment
            self.fields['line_items'].queryset = self.instance.line_items.all()

    @staticmethod
    def label_from_instance(obj):
        return f"LineItem #{obj.id} - {obj.product_name} (Qty: {obj.quantity}) - ${obj.price}"
    
class ShipmentEditForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'status': 'Shipment Status'
        }