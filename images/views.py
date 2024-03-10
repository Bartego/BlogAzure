import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
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

from django.core.mail import send_mail
import os
from .forms import ContactForm

logger = logging.getLogger(__name__)


def about(request):
    return render(request, 'images/about.html', {'title':'About'})
def hobby(request):
    return render(request, 'images/hobby.html', {'title':'Hobby'})


class PostListView(ListView):
    model = Post
    template_name = 'images/index.html' # <app>/<model_name>_<viewtype-'list' as example>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()  # Add the form to the context
        return context



class UserPostListView(ListView):
    model = Post
    template_name = 'images/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post
    template_name = 'images/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'images/post_form.html'
    fields = ['title','content','post_image']

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
    # template_name = 'images/g_post_confirm_delelte.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = 'From: ' + from_email + '\n\nMessage:\n' + form.cleaned_data['message']
            send_mail(subject, message, from_email, [os.getenv('EMAIL_USER')])
        return render(request, 'images/contact.html', {'form': form, 'message': 'Your message has been sent to matej.radosovsky@gmail.com. Thank you, I\'ll contact you as soon as possible.'})
    else:
        form = ContactForm()
    return render(request, 'images/index.html', {'form': form})
    