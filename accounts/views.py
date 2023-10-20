from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_http_methods
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

@require_http_methods(["GET", "POST"])
def login(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('boards:index')
    form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/login.html', context)


@require_http_methods(["POST"])
def logout(request):
    auth_logout(request)
    return redirect('boards:index')

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('boards:index')
    form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html',context)


# 프로필
@require_http_methods(["GET"])
def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    context = {
        'person':person
    }
    return render(request, 'accounts/profile.html',context)


# 팔로우 데이터 저장 및 팔로우 데이터 삭제
@require_http_methods(["POST"])
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)  # 글 주인
    me = request.user   # 나
    if me != you:
        if me in you.followers.all():   # 만약에 글 주인 팔로워 리스트에 내가 있다면
            you.followers.remove(me)  # 날 삭제해줘 = 팔로우 취소
        else:
            you.followers.add(me)   # 없다면, 날 추가해줘
    return redirect('accounts:profile', you.username)