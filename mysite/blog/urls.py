from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/renove', views.PostDeleteView.as_view(), name='post_remove'),
    path('drafts', views.DraftListView.as_view(), name='post_draft_list'),

]
