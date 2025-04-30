from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()  # Query all products from the database
    return render(request, 'store/product_list.html', {'products': products})

def home(request):
    return render(request, 'store/home.html')