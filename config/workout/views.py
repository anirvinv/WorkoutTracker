from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *

def index(request):
    if request.method=="POST":
        if "key" in request.POST:
            key = request.POST['key']
            request.user.exercises.get(pk=key).delete()
            return redirect('home')
        else:
            form = ExerciseForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                volume = form.cleaned_data['volume']
                exercise = Exercise(user=request.user, name=name, volume=volume)
                exercise.save()
                return redirect('home')
            else:
                return render(request, 'workout/index.html', context={'form': form})
    else:
        if request.user.is_authenticated:
            exercises = request.user.exercises.all()
        else:
            exercises = []
    return render(request, 'workout/home.html', context={'form': ExerciseForm(), 'exercises': exercises})

def summary(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=="POST":
        if 'update' in request.POST:
            key = request.POST['key']
            new_height = request.POST['height']
            new_weight = request.POST['weight']
            Stats.objects.filter(pk=key).update(height=new_height, weight=new_weight)
            return redirect('summary')
        elif 'remove' in request.POST:
            key = request.POST['key']
            Stats.objects.filter(pk=key).delete()
        else:
            form = StatsForm(request.POST)
            if form.is_valid():
                height = form.cleaned_data['height']
                weight = form.cleaned_data['weight']
                Stats.objects.create(user=request.user, height=height, weight=weight)
            else:
                return render(request, 'workout/summary.html', context={'form': form})
            
    return render(request, 'workout/summary.html', context={'form': StatsForm(), 'stat_list': request.user.stats.all()})

def account(request):
    return render(request, 'workout/account.html', context={
        'username': request.user.username,
    })

def log_in(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'workout/login.html', context={'form': LoginForm()})
    return render(request, 'workout/login.html', context={'form': LoginForm()})

def log_out(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # login(request, request.user)
            return redirect('login')
        return render(request, 'workout/signup.html', context={'form': form})
    return render(request, 'workout/signup.html', context={'form': UserCreationForm()})