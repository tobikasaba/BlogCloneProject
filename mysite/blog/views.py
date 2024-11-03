from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

from mysite.blog.forms import PostForm
from mysite.blog.models import Post


# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        """
        Retrieve the list of published posts.

        This method runs a query on the Post model (Python version of running an SQL query).
        This grabs the Post model and filters it based on the specified conditions.
        __lte is a django functionality which stands for less than or equals to.
        Hence, this queryset fetches posts with a published_date that is less than or equal to the current time.
        The results are ordered by published_date in descending order.
        This is denoted by the "-" prefix on published date.

        Returns:
        QuerySet: A queryset of Post objects.
        """
        return Post.objects.filter(
            published_date__lte=timezone.now()).order_by('-published_date')


"""
Glossary of terms, attributes and variables

LoginRequiredMixin: s a mixin provided by Django that is used to restrict access to a view, 
ensuring that only authenticated users can access it.  If a user is not logged in and tries to access a view that uses
this mixin, they will be redirected to the login page.

form_class: specifies which form to use for handling user input. This is particularly useful when creating or 
editing model instances through forms. The form_class attribute indicates which form to use when rendering 
the view and processing form submissions.

redirect_field_name: this attribute is used to specify the name of the query parameter that will hold the URL to which
the user should be redirected after logging in. This is particularly relevant when using the LoginRequiredMixin.
That is, after login in the user is redirected to the page specified by redirect_field_name

success_url: this attribute defines where users will be redirected after successfully completing an action on the view.
This is only done after the action on the view has been completed which in this case is deleting a post.

reverse_lazy: this is used to hard code success_url with the url that dynamically generates based on some criteria.
"""


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    # redirect users to the detail view once they've logged in
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    # only activated after the post has been deleted
    success_url = reverse_lazy('blog:post_list')
    model = Post


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')
