from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import AuthorPermission
from .serializers import (
    GroupSerializer,
    PostSerializer,
    CommentSerializer,
    FollowSerializer
)
from posts.models import Group, Post


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet только для чтения и работы с Группами."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с Публикациями."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorPermission, IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """
        Сохраняет создаваемую публикацию с указанием
        текущего пользователя в качестве автора.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с Комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (AuthorPermission, IsAuthenticatedOrReadOnly)

    def get_post(self):
        """Получает объект поста, к которому привязан комментарий."""
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Получает queryset всех комментариев к конкретному посту."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Создает новый комментарий, привязанный к конкретному посту."""
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для работы с Подписками."""

    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Получает запрос для списка подписчиков пользователя.."""
        return self.request.user.subscribers.all()

    def perform_create(self, serializer):
        """Выполняет создание подписки."""
        serializer.save(user=self.request.user,)
