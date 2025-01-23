from django.db import models
from django.contrib.auth.models import User


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

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts")
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True,
                              null=True, related_name="posts")

    def __str__(self):
        """
        Return a string representation of the post instance.

        Returns:
            str: The username of the author and the first 20 characters of the
            post text.
        """
        return f"{self.author.username}: {self.text[:20]}..."


