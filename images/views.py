import logging

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

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

posts = [
    {
        'author': 'Matej',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Jan 27, 2024'
    },
    {
        'author': 'JurajR',
        'title': 'Blog Post 2',
        'content': 'Birthday post content',
        'date_posted': 'Feb 5, 2024'
    }
]


def home(request):
    context = {
        'posts': Post.objects.all() # common error -> 'post':posts wont work as .html files loop over 'posts' not 'post' 
    }
    return render(request, 'images/home.html', context)


def about(request):
    return render(request, 'images/about.html', {'title':'About'})