from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .models import Tweet
from .forms import TweetForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

class LoginView(auth_views.LoginView):
    template_name = 'login.html'

@login_required
def feed(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user.profile
            tweet.save()
            return redirect('feed')
    else:
        form = TweetForm()
    tweets = Tweet.objects.all()
    return render(request, 'social/feed.html', {'form': form, 'tweets': tweets})