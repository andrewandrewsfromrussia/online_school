from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSelfOrReadOnly(BasePermission):
    """
    Разрешает:
    - смотреть (GET/HEAD/OPTIONS) любой профиль,
    - изменять (PUT/PATCH/DELETE) только свой.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj
