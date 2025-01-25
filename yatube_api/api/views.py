from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from posts.models import Post, Comment, Follow, Group
from .serializers import (PostSerializer, CommentSerializer,
                          FollowSerializer, GroupSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from rest_framework.exceptions import PermissionDenied
from .paginators import PostPagination
from rest_framework.filters import SearchFilter
from django.db.models import Q
from rest_framework.response import Response

class PostViewSet(ModelViewSet):
    """ViewSet for managing posts."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = PostPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Пытаемся применить пагинацию
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            raise PermissionDenied("Удалить публикацию может только её автор.")
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
    """
    ViewSet for managing comments.

    Handles CRUD operations for comments, including:
        - Listing comments associated with a specific post.
        - Creating new comments for a post.
        - Retrieving, updating, and deleting specific comments.

    Methods:
        - get_queryset(): Filters comments by the post ID from the URL.
        - perform_create(serializer): Associates the new comment with the
          authenticated user and the specified post.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Retrieve the queryset of comments for a specific post.

        Filters comments by the `post_id` parameter in the URL.

        Returns:
            QuerySet: A queryset containing comments for the specified post.
        """
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """
        Saves a new comment instance.

        Associates the comment with the authenticated user and the post ID
        from the URL.

        Args:
            serializer (CommentSerializer): The serializer containing validated
            data for the comment.

        Returns:
            None
        """
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)


class FollowViewSet(ModelViewSet):
    """
    ViewSet for managing follows.
    Only authenticated users can access this endpoint.
    """

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        """
        Optionally restricts the returned follows to a filtered subset.

        based on query parameters.
        """
        queryset = super().get_queryset()
        following_username = (
            self.request.query_params.get('search', None)
        )
        if following_username:
            queryset = queryset.filter(
                Q(following__username__icontains=following_username)
            )

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically set the user to the authenticated user.
        and check for duplicate follows.
        """
        user = self.request.user
        following = serializer.validated_data['following']
        # Запрет на подписку на самого себя
        if user == following:
            raise ValidationError("Вы не можете подписаться на самого себя.")

        # Проверяем, существует ли уже подписка
        if Follow.objects.filter(user=user, following=following).exists():
            raise ValidationError("Вы уже подписаны на этого пользователя.")

        # Создаем новую подписку
        serializer.save(user=user)


class GroupViewSet(ReadOnlyModelViewSet):
    """ViewSet for managing groups."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
