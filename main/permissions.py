from rest_framework import permissions


class PortfolioUserPermission(permissions.BasePermission):
    """Check if current user is portfolio owner"""
    message = "Portfolio belongs to other user"

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' or request.user.pk == obj.user.pk:
            return True
        return False


class ProjectContactUserPermission(permissions.BasePermission):
    """Check if current user is portfolio owner"""
    message = "Portfolio belongs to other user"

    def has_object_permission(self, request, view, obj):
        if request.user.pk == obj.portfolio.user.pk:
            return True
        return False
