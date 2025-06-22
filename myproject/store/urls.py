from django.contrib import admin
from django.urls import path, include
from store import views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('purchase/', views.purchase, name='purchase'),
    #path('purchase/<int:transaction_id>/', views.purchase_detail, name='purchase_detail'),
    path('account/', views.account_view, name='account'),
    path('invoice/<int:transaction_id>/', views.invoice_detail, name='invoice_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('internal-tools/', views.internal_tools, name='internal_tools'),
    path('catalog/', views.catalog_tool, name='catalog_tool'),
    path('catalog/add/', views.add_product, name='add_product'),
    path('catalog/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('shipments/', views.shipment_tool, name='shipment_tool'),
    path('shipments/add/', views.add_shipment, name='add_shipment'),
    path('shipments/edit/<int:shipment_id>/', views.edit_shipment, name='edit_shipment'),
    path('api/transaction-line-items/<int:transaction_id>/', views.get_transaction_line_items, name='get_transaction_line_items'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Append the list correctly