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

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),

    # UI Pages
    path('', home, name='home'),
    path('products/public/', public_products_page, name='public-products-page'),
    path('chat/', chatbot_page, name='chat-page'),

    # API
    path('api/', include('product_marketplace.api_urls')),
]

