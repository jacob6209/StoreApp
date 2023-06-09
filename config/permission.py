import requests
from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated() and request.user.is_admin
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated():
            return False

        if view.action == 'retrieve':
            return obj == request.user or request.user.is_admin
        elif view.action in ['update', 'partial_update']:
            return obj == request.user or request.user.is_admin
        elif view.action == 'destroy':
            return obj == request.user or request.user.is_admin
        else:
            return False

class ProductViewSetPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['retrieve','list']:
            return True
        elif view.action in ['create','retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_superuser
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        elif view.action in ['update', 'partial_update','destroy']:
            return request.user.is_superuser
        else:
            return False

class CategoriViewSetPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['create','retrieve','list', 'update', 'partial_update', 'destroy']:
            return request.user.is_superuser
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve','update', 'partial_update','destroy']:
            return request.user.is_superuser
        else:
            return False

class ReviewViewSetPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['retrieve','list']:
            return True
        elif view.action in ['create','update', 'partial_update', 'destroy']:
            return request.user.is_authenticated or request.user.is_superuser
        else:
            return False

    def has_object_permission(self, request, view, obj):

        # Deny actions on objects if the user is not authenticated

        if not request.user.is_authenticated:
            return False
        elif view.action in ['retrieve','list']:
            return True
        elif view.action in ['retrieve','list','update', 'partial_update','destroy']:
            return obj.user== request.user or request.user.is_superuser
        else:
            return False
