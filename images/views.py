import logging

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import (ListView,
                                DetailView,
                                CreateView,
                                UpdateView,
                                DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from images.forms import UploadForm
from images.models import Image, Post
from images.tables import ImageTable


logger = logging.getLogger(__name__)


def index_view(request):
    images = Image.objects.all()
    image_table = ImageTable(images)
    upload_form = UploadForm()

    return render(request, 'images/index.html', {
        'images': images,
        'image_table': image_table,
        'upload_form': upload_form,
    })


@require_http_methods(["POST"])
def upload_view(request):
    upload_form = UploadForm(data=request.POST, files=request.FILES)

    if upload_form.is_valid():
        upload_form.save(commit=True)
    else:
        logger.warning("Something went wrong with uploading the file.")
        logger.warning(request.POST)
        logger.warning(request.FILES)

    return redirect('images-index')



def home(request):
    context = {
        'posts': Post.objects.all() # common error -> 'post':posts wont work as .html files loop over 'posts' not 'post' 
    }
    return render(request, 'images/home.html', context)

def about(request):
    return render(request, 'images/about.html', {'title':'About'})


class PostListView(ListView):
    model = Post
    template_name = 'images/home.html' # <app>/<model_name>_<viewtype-'list' as example>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    #following code will owerride default behaviour and post will be created with user that is currently loged
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    #following code will owerride default behaviour and post will be created with user that is currently loged
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    