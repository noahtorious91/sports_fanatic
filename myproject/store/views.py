from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import random

# Query all products from the database - used on the product list page
def product_list(request):
    products = Product.objects.all()  # Query all products from the database
    return render(request, 'store/product_list.html', {'products': products})

# Query a random subset of products via the database - used on the home page
def home(request):
    # Fetch all products and select a random subset
    products = list(Product.objects.all())
    random_products = random.sample(products, min(len(products), 5))  # Show up to 5 random products
    return render(request, 'store/home.html', {'random_products': random_products})

# Gets the cart from the session and Gets the products in the cart
def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    for product in products:
        quantity = cart[str(product.id)]
        total_price = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)]
        })
    return render(request, 'store/cart.html', {'cart_items': cart_items})

# Add to cart function - gets the product ID from the request and gets the cart or an empty dictionary
# and adds the product to the cart, incrementing the quanitity of items if it already exists
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {}) 
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

# Remove from cart function - gets the product ID fromt the request and gets the cart or an empty dictionary
# and removes the product from the cart, deleting all the items and then saving the state of the cart. 
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

# Custom User Creation Form - Subclass of the UserCreationForm to add custom styling
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm your password'
            })

        }


    
