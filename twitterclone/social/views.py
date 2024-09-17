from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Profile, Tweet
from .forms import RegisterForm, TweetForm, LoginForm
from .serializers import ProfileSerializer, TweetSerializer, UserSerializer

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

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class FeedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        else:
            return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)