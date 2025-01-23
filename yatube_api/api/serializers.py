from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from posts.models import Comment, Post, Follow, Group
from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """
    Serialize and deserialize Post instances.

    Converts Post model instances into JSON format and vice versa.
    Includes fields such as author, text, pub_date, and image.
    """

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        """
        Meta options for PostSerializer.

        Specifies the model and fields to include in serialization.
        """

        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """
    Serialize and deserialize Comment instances.

    Converts Comment model instances into JSON format and vice versa.
    Includes fields such as author, post, text, and created date.
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        """
        Meta options for CommentSerializer.

        Specifies the model and fields to include in serialization.
        """

        fields = ['id', 'author', 'text', 'created', 'post']
        read_only_fields = ['post', 'author', 'created']
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follow model.

    Converts Follow instances into JSON format and vice versa.
    """

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ['user', 'following']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
