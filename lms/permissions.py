from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """
    Доступ только пользователям из группы 'moderators'.
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            user
            and user.is_authenticated
            and user.groups.filter(name='moderators').exists()
        )

class IsOwner(BasePermission):
    """
    Доступ только владельцу объекта (поле owner).
    """

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "owner", None) == request.user