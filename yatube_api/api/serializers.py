from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


from posts.models import Comment, Group, Post, Follow, User


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с Группами."""

    class Meta:
        fields = '__all__'
        model = Group


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с Публикациями."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('id', 'pub_date', 'author')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с Комментариями."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с Подписками."""

    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                Follow.objects.all(),
                ('user', 'following'),
                message='Подписка уже успешно оформлена'
            ),
        ]

    def validate(self, data):
        """Проверяет данные подписки."""
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Пользователь не может подписаться на самого себя :('
            )
        return data
