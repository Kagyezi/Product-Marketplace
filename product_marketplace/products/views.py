from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from .models import Product
from .serializers import ProductSerializer
from .permissions import CanEditProduct, CanApproveProduct

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(business=user.business)

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            business=self.request.user.business,
            status='pending'
        )

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [CanEditProduct()]
        if self.action == 'approve':
            return [CanApproveProduct()]
        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        product = self.get_object()
        product.status = 'approved'
        product.save()
        return Response({'message': 'Product approved'})


class PublicProductListView(ListAPIView):
    queryset = Product.objects.filter(status='approved')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
