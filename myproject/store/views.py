from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from .models import Transaction, LineItem, Product, Shipment
from .forms import ProductForm, ShipmentForm, ShipmentEditForm
from django.db import transaction
from django.http import JsonResponse
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
    cart = request.session.get('cart', {})  # Retrieve cart from session
    products = Product.objects.filter(id__in=cart.keys())  # Fetch products in the cart
    cart_items = []
    subtotal = 0

    # Build cart items and calculate subtotal
    for product in products:
        quantity = cart[str(product.id)]
        total_price = product.price * quantity
        subtotal += total_price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })

    # Calculate taxes and total
    tax_rate = Decimal('0.10')  # 10% tax
    taxes = subtotal * tax_rate
    total = subtotal + taxes

    # Pass data to the template
    context = {
        'cart_items': cart_items,
        'subtotal': round(subtotal, 2),
        'taxes': round(taxes, 2),
        'total': round(total, 2),
    }
    return render(request, 'store/cart.html', context)

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

def cart_view(request):
    cart_items = request.session.get('cart', [])  # Example: Retrieve cart items from session
    subtotal = sum(item['product_price'] * item['quantity'] for item in cart_items)
    tax_rate = Decimal('0.10')  # 10% tax
    taxes = subtotal * tax_rate
    total = subtotal + taxes

    print(f"Subtotal: {subtotal}, Taxes: {taxes}, Total: {total}")

    context = {
        'cart_items': cart_items,
        'subtotal': round(subtotal, 2),
        'taxes': round(taxes, 2),
        'total': round(total, 2),
    }
    return render(request, 'store/cart.html', context)

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

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty')
        return redirect('cart')

    # Create a transaction
    with transaction.atomic():
        new_transaction = Transaction.objects.create(
            user=request.user,
            status='pending',  # Default status
            promotion_version_id=None  # Set this if applicable
        )

        # Create line items for each product in the cart
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            LineItem.objects.create(
                transaction=new_transaction,
                product=product,
                product_name=product.name,
                price=product.price,
                quantity=quantity,
                tax_rate=round(Decimal('0.10'), 2)
            )

        # Update transaction status to 'pending'
        new_transaction.status = 'pending'
        new_transaction.save()

    # Clear the cart
    request.session['cart'] = {}
    messages.success(request, 'Purchase successful!')

    return redirect('account')

@login_required
def purchase_summary(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    line_items = LineItem.objects.filter(transaction=transaction)

    subtotal = sum(item.price * item.quantity for item in line_items)
    taxes = sum(item.price * item.quantity * item.tax_rate for item in line_items)
    total = subtotal + taxes

    return render(request, 'store/purchase_summary.html', {
        'transaction': transaction,
        'line_items': line_items,
        'subtotal': round(subtotal, 2),
        'taxes': round(taxes, 2),
        'total': round(total, 2),
    })

def get_transaction_line_items(request, transaction_id):
    """API endpoint to get line items for a specific transaction"""
    try:
        line_items = LineItem.objects.filter(transaction__transaction_id=transaction_id)
        
        data = []
        for item in line_items:
            data.append({
                'id': item.id,
                'product_name': item.product_name,
                'quantity': item.quantity,
                'price': str(item.price),
                'transaction_id': item.transaction.transaction_id
            })
        
        return JsonResponse({'line_items': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'store/login.html')

@login_required
def account_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    transaction_summaries = []

    for transaction in transactions:
        line_items = LineItem.objects.filter(transaction=transaction)
        subtotal = sum(item.price * item.quantity for item in line_items)
        taxes = sum(item.price * item.quantity * item.tax_rate for item in line_items)
        total = subtotal + taxes

        transaction_summaries.append({
            'transaction': transaction,
            'subtotal': round(subtotal, 2),
            'taxes': round(taxes, 2),
            'total': round(total, 2),
            'line_items': line_items
        })
    return render(request, 'store/account.html', {'transaction_summaries': transaction_summaries})

@login_required
def invoice_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    line_items = LineItem.objects.filter(transaction=transaction)
    return render(request, 'store/invoice.html', {'transaction': transaction, 'line_items': line_items})

@login_required
def internal_tools(request):
    return render(request, 'store/internal_tools.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def catalog_tool(request):
    products = Product.objects.all()
    return render(request, 'store/catalog_tool.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('catalog_tool')
    else:
        form = ProductForm()  # Handle GET request by rendering an empty form
    return render(request, 'store/add_product.html', {'form': form})
    
@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog_tool')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form, 'product': product})

@login_required
def shipment_tool(request):
    shipments = Shipment.objects.all().order_by('-created_at')
    return render(request, 'store/shipment_tool.html', {'shipments': shipments})

@login_required
def add_shipment(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save()
            # Handle line items if they exist
            line_items = request.POST.getlist('line_items')
            if line_items:
                shipment.line_items.set(LineItem.objects.filter(id__in=line_items))
            messages.success(request, f'Shipment {shipment.shipment_id} created successfully!')
            return redirect('shipment_tool')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ShipmentForm()
    
    return render(request, 'store/add_shipment.html', {'form': form})
    
@login_required
def edit_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, shipment_id=shipment_id)
    if request.method == 'POST':
        form = ShipmentEditForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            messages.success(request, "Shipment updated successfully")
            return redirect('shipment_tool')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ShipmentEditForm(instance=shipment)
    return render(request, 'store/edit_shipment.html', {'form': form, 'shipment': shipment})