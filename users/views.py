from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,
                             f'Your account has been created for {username}! You are now able to log in.')
            return redirect('login')
            # password = form.cleaned_data.get('passwrod')
    else:
        form = UserRegisterForm()
        # watch for () at the ned of the class
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    '''
    if you are goint to update profile data, you need to update user form and profile form, if you get 
    POST request, instance is the one of current loged user
    '''
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
        messages.success(request, f'Your account has been updated.')
        return redirect('profile')
  
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        # there needs to be request.user.profile because profile is mapped to user and it wont work without 'user' in the middile.
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)