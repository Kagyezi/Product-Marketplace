"""
URL configuration for product_marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from products.views import public_products_page
from chatbot.views import chatbot_page
from accounts.views import login_view, logout_view
from products.views import internal_products, approve_product_ui, create_product
from products.views import edit_product, delete_product


def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),

    # UI Pages
    path('', home, name='home'),
    path('products/public/', public_products_page, name='public-products-page'),
    path('chat/', chatbot_page, name='chat-page'),

    path("login/", login_view),
    path("logout/", logout_view),

    path("products/internal/", internal_products, name="internal-products"),
    path("products/<int:product_id>/approve/", approve_product_ui),
    path("products/create/", create_product, name="create-product"),
    path("products/<int:product_id>/edit/", edit_product, name="edit-product"),
    path("products/<int:product_id>/delete/", delete_product, name="delete-product"),

    # API
    path('api/', include('chatbot.urls')),
]

