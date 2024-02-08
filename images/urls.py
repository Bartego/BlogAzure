from django.urls import path
from .views import PostListView

from . import views

urlpatterns = [
    path('image_upload', views.index_view, name='images-index'),
    path('upload/', views.upload_view, name='images-upload'),
    path('', PostListView.as_view(), name='blog-home'),
    # path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
]