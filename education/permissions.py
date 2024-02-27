from rest_framework.permissions import BasePermission


class Moderator(BasePermission):
    message = 'Несоответствие прав доступа.'

    def has_permission(self, request, view):
        return request.user.is_moderator


class Author(BasePermission):
    message = 'Только для авторов.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author