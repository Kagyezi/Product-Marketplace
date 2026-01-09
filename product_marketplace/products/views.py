from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden

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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


def public_products_page(request):
    # products = Product.objects.filter(status='approved')
    products = Product.objects.all()
    return render(request, 'public_products.html', {
        'products': products
    })

@login_required
def internal_products(request):
    products = Product.objects.filter(business=request.user.business)
    return render(request, "internal_products.html", {"products": products})

@login_required
def approve_product_ui(request, product_id):
    if request.user.role not in ["ADMIN", "APPROVER"]:
        return HttpResponseForbidden("Not allowed")

    product = Product.objects.get(id=product_id)
    product.status = "approved"
    product.save()

    return redirect("internal-products")

@login_required
def admin_dashboard(request):
    if request.user.role != "ADMIN":
        return HttpResponseForbidden("Admins only")

    products = Product.objects.filter(
        business=request.user.business
    )

    return render(request, "admin_dashboard.html", {"products": products})


@login_required
def create_product(request):
    # Role check
    if request.user.role not in ["ADMIN", "EDITOR"]:
        return HttpResponseForbidden("You are not allowed to create products.")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            business=request.user.business
        )


        return redirect("internal-products")

    return render(request, "create_product.html")

@login_required
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)

    # Business isolation
    if product.business != request.user.business:
        return HttpResponseForbidden("Not your business product.")

    # Role check
    if request.user.role not in ["ADMIN", "EDITOR"]:
        return HttpResponseForbidden("You are not allowed to edit products.")

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        # product.status = "pending"  # re-approval required
        product.save()

        return redirect("internal-products")

    return render(request, "edit_product.html", {"product": product})

@login_required
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)

    # Business isolation
    if product.business != request.user.business:
        return HttpResponseForbidden("Not your business product.")

    # Role check
    if request.user.role not in ["ADMIN", "EDITOR"]:
        return HttpResponseForbidden("You are not allowed to delete products.")

    if request.method == "POST":
        product.delete()
        return redirect("internal-products")

    return render(request, "delete_product.html", {"product": product})

@login_required
def viewer_products(request):
    if request.user.role != "VIEWER":
        return HttpResponseForbidden("Viewers only")

    products = Product.objects.all()
    return render(request, "viewer_products.html", {"products": products})
