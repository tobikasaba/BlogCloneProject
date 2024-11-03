from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    # super users has the ability to create, edit and delete posts
    # linking the author to an authorisation user ensures this
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    # can be left blank or empty
    published_date = models.DateTimeField(blank=True, null=True)

    # a publish button to be created and whenever thr button is clicked, it calls this function which sets the publish date
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # returns the approved comments from the blog post. i.e. comments from the Comment class that have been approved
    def approve_comments(self):
        return self.comments.filter(approved_comments=True)

    # once a post has been created, the site returns you to the url named post_detail with the specific pk
    # i.e. {post_detail}/{pk}
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    # this connects a comment to a post i.e. each comment is aligned to a post.
    # Post can be directly referenced here instead of 'blog.Post' because they are in the same app and models.py file
    # if the Post model were in another app, you would need to use the {app name}.{Model Class}
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    approved_comments = models.BooleanField(default=False)

    def approve(self):
        self.approved_comments = True
        self.save()

    # once a comment has been created, the site returns you to the url named post_list
    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
