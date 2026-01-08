from rest_framework.permissions import BasePermission

class CanEditProduct(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['ADMIN', 'EDITOR']


class CanApproveProduct(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['ADMIN', 'APPROVER']
