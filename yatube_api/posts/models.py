from django.contrib.auth import get_user_model
from django.db import models

from .constants import SUMBOLS_LENGTH

User = get_user_model()


class Group(models.Model):
    """Модель для описания Группы."""

    title = models.CharField(
        'Заголовок',
        max_length=200
    )
    slug = models.SlugField(
        'Идентификатор',
        unique=True
    )
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title[:SUMBOLS_LENGTH]


class Post(models.Model):
    """Модель для описания Публикации."""

    text = models.TextField('Текст поста')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='posts'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='posts/',
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return self.text[:SUMBOLS_LENGTH]


class Comment(models.Model):
    """Модель для описания Комментария."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField('Текст комментария')
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:SUMBOLS_LENGTH]


class Follow(models.Model):
    """Модель для описания Подписки."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_user_and_subscribers'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("following")),
                name='user_cant_self_follow',
            ),
        ]

    def __str__(self):
        return ('{} имеет подписку на {}'.
                format(self.following, self.user))
