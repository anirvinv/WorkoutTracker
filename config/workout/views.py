from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *


def index(request):
    if request.method == "POST":
        if "remove" in request.POST:
            key = request.POST['key']
            request.user.exercises.get(pk=key).delete()
            return redirect('home')
        elif "update" in request.POST:
            name = request.POST['name']
            volume = request.POST['volume']
            rpe = request.POST['rpe']
            exercise_type = request.POST['exercise_type']
            key = request.POST['key']
            Exercise.objects.filter(pk=key).update(
                name=name, volume=volume, rpe=rpe, exercise_type=exercise_type)
            return redirect('home')
        else:
            form = ExerciseForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                volume = form.cleaned_data['volume']
                rpe = form.cleaned_data['rpe']
                exercise_type = request.POST['exercise_type']
                exercise = Exercise(user=request.user,
                                    name=name, volume=volume,
                                    rpe=rpe, exercise_type=exercise_type)
                exercise.save()
                return redirect('home')
            else:

                return render(request, 'workout/index.html', context={'form': form})
    else:
        if request.user.is_authenticated:
            exercises = request.user.exercises.all()
            exercise_dates = {}
            for exercise in exercises:
                date = f"{exercise.date.month}/{exercise.date.day}/{exercise.date.year}"
                # date = f"{exercise.date.time()}"
                if date in exercise_dates.keys():
                    exercise_dates[date] += [exercise]
                    # pass
                else:
                    exercise_dates[date] = [exercise]
        else:
            exercise_dates = {}
    return render(request, 'workout/home.html', context={'form': ExerciseForm(), 'exercise_dates': exercise_dates.items()})


def weighttracker(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        if 'update' in request.POST:
            key = request.POST['key']
            new_height = request.POST['height']
            new_weight = request.POST['weight']
            Stats.objects.filter(pk=key).update(
                height=new_height, weight=new_weight)
            return redirect('weighttracker')
        elif 'remove' in request.POST:
            key = request.POST['key']
            Stats.objects.filter(pk=key).delete()
        else:
            form = StatsForm(request.POST)
            if form.is_valid():
                height = form.cleaned_data['height']
                weight = form.cleaned_data['weight']
                Stats.objects.create(
                    user=request.user, height=height, weight=weight)
            else:
                return render(request, 'workout/weighttracker.html', context={'form': form})

    return render(request, 'workout/weighttracker.html', context={'form': StatsForm(), 'stat_list': request.user.stats.all()})


def account(request):
    return render(request, 'workout/account.html', context={
        'username': request.user.username,
    })


def log_in(request):
    if request.method == "POST":
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
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # login(request, request.user)
            return redirect('login')
        return render(request, 'workout/signup.html', context={'form': form})
    return render(request, 'workout/signup.html', context={'form': UserCreationForm()})
