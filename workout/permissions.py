from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class IsObjectVisible(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj.public and request.user != obj.creator:
            return False
        return True

class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user
