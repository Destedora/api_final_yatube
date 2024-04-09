from django.contrib import admin

from .models import Comment, Group, Post, Follow

admin.site.empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройка раздела Публикации."""

    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Настройка раздела Группы."""

    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка раздела Комментарии."""

    list_display = ('pk', 'post', 'text', 'author', 'created')
    search_fields = ('author',)
    list_filter = ('created',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Настройка раздела Подписки."""

    list_display = ('user', 'following')
    search_fields = ('user__username', 'following__username')
    ordering = ('user',)
