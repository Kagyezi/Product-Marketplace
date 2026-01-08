from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from products.views import ProductViewSet, PublicProductListView
from chatbot.views import ChatbotView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Authentication
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),

    # Product APIs
    path('', include(router.urls)),
    path('products/public/', PublicProductListView.as_view(), name='public-products'),

    # Chatbot API
    path('chat/', ChatbotView.as_view(), name='chatbot'),
]

