from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .models import Tweet
from .forms import RegisterForm, TweetForm, LoginForm

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

class LoginView(auth_views.LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form.error_message = "Login ou senha incorretos."
        return self.render_to_response(self.get_context_data(form=form))

@login_required
def feed(request):
    if request.method == 'POST':
        if 'delete_tweet' in request.POST:
            tweet_id = request.POST.get('tweet_id')
            tweet = get_object_or_404(Tweet, id=tweet_id)
            if tweet.author != request.user.profile:
                return HttpResponseForbidden("Você não tem permissão para deletar este tweet.")
            tweet.delete()
            return redirect('feed')
        else:
            form = TweetForm(request.POST)
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.author = request.user.profile
                tweet.save()
                return redirect('feed')
    else:
        form = TweetForm()
    tweets = Tweet.objects.all()
    return render(request, 'feed.html', {'form': form, 'tweets': tweets})

