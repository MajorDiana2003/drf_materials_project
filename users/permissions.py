from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Разрешает доступ только владельцу профиля"""
    def has_object_permission(self, request, view, obj):
        # Проверяем, совпадает ли текущий пользователь с объектом профиля
        return obj == request.user
