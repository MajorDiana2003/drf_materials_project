from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """Проверяет, входит ли пользователь в группу модераторов"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='модераторы').exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем объекта"""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
