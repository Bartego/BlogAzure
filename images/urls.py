from django.urls import path
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
)

from . import views

urlpatterns = [
   # path('image_upload', views.index_view, name='images-index'), #old project
   # path('upload/', views.upload_view, name='images-upload'), # old project
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    # path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
]