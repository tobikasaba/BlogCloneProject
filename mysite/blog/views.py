from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

from .forms import PostForm, CommentForm
from .models import Post, Comment


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


########################################################
########################################################
"""
This section makes use of Function based views FBVs

get_object_or_404(): This  used for getting an object from a database using a model’s manager.
It raises an Http404 exception if the object is not found. 
The Post object gotten is based on the primary key (pk) f the post.
This is particularly useful for ensuring the post with the pk exists before attempting to publish it.
"""


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=post.pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # if the form is sending data to the server via a POST request
    if request.method == 'POST':
        # Initialises the form with submitted data (stores the data in the from variable)
        form = CommentForm(request.POST)
        if form.is_valid():
            # creates a new Comment instance but does not save it to the database yet.
            # This is useful because we want to modify the instance
            # (specifically, we want to assign it to the post) before saving it.
            comment = form.save(commit=False)
            # post is a foreign key in the CommentForm Model.
            # this assigns the post field in the comment to the post retrieved using get_object_or_404()
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)

    # if the form is not sending any data, initialise the form and render it on the html template
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', context={'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    # after deleting comment, django no longer has access the primary key of the post
    # this is why the primary key of the post is stored in a separate variable 'post_pk'
    # this makes the primary key of the post associated with the comment accessible.
    return redirect('blog:post_detail', pk=post_pk)
