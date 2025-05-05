from rest_framework import permissions


class ModeratorPermission(permissions.BasePermission):
    """Проверка на то, что пользователь модератор."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()


class CreatorPermission(permissions.BasePermission):
    """Проверка на то, что пользователь создатель курса или урока."""
    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user:
            return True
        return False


class UserHimself(permissions.BasePermission):
    """Проверка на то, что пользователь редактирует свой профиль."""
    def has_object_permission(self, request, view, obj):
        if obj.email == request.user.email:
            return True
        return False