from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from posts.models import Comment, Post


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

        fields = '__all__'
        model = Comment
