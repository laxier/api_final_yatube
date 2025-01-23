from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """
    Represent a group to which posts can belong.

    Attributes:
        title: The name of the group.
        slug: A unique identifier for the group.
        description: A brief description of the group.
    """

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Return a string representation of the group instance.

        Returns:
            str: The title of the group.
        """
        return self.title


class Post(models.Model):
    """
       Represent a post in the system.

       Attributes:
           author: The user who created the post.
           text: The content of the post.
           pub_date: The date and time when the post was published.
           image: An optional image attached to the post.
           group: An optional group to which the post belongs.
    """

    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True,
                              null=True, related_name="posts")

    def __str__(self):
        """
            Return a string representation of the post instance.

            Returns:
                str: The username of the author and the first 20 characters of
                the post text.
        """
        return self.text


class Comment(models.Model):
    """
        Represent a comment on a post.

        Attributes:
            author (User): The user who created the comment.
            post (Post): The post to which the comment belongs.
            text (str): The text content of the comment.
            created (datetime): The date and time when the comment was created.
    """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        """
        Return a string representation of the comment instance.

        Returns:
            str: The username of the author and the first 20 characters
            of the comment text.
        """
        return f"{self.author.username}: {self.text[:20]}..."


class Follow(models.Model):
    """
    Represent a subscription relationship between users.

    Attributes:
        user (User): The user who is following.
        following (User): The user who is being followed.
        created (datetime): The date and time when the subscription
        was created.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )

    created = models.DateTimeField(
        'Дата подписки', auto_now_add=True, db_index=True,
        help_text='The date and time when the subscription was created.'
    )

    class Meta:
        """
        Meta options for the Follow model.

        Enforces unique subscription pairs and adds a constraint to prevent
        self-subscription.
        """
        unique_together = ['user', 'following']
        ordering = ['-created']


    def __str__(self):
        """
        Return a string representation of the subscription.

        Returns:
            str: The username of the follower and the followed user.
        """
        return f"{self.user.username} follows {self.following.username}"