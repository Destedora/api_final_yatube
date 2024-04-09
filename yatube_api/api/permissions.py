from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorPermission(BasePermission):
    """Проверка разрешения для автора объекта."""

    def has_object_permission(self, request, view, obj):
        """Проверяет разрешение на доступ к конкретному объекту."""
        return (request.method in SAFE_METHODS
                or request.user == obj.author)
