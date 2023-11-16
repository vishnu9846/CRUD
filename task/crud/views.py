from django.shortcuts import render,get_object_or_404,redirect
from .models import Task,Registration
from django.contrib import messages
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login  

from rest_framework import viewsets
from .serializers import TaskSerializer

def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('crud:task')
            else:
                messages.error(request, "Invalid credentials")
                return redirect('crud:index')
            
            messages.error(request, "Invalid credentials")
            return redirect('crud:index')
        else:
            error_messages = form.errors
            for field, error in error_messages.items():
                messages.error(request, f"{field}: {error}")
            return redirect('crud:index')
    else:
        form = LoginForm()

    return render(request, 'register/index.html', {'form': form})

def reg(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirmpassword = form.cleaned_data['confirmpassword']
            
            if password != confirmpassword:
                messages.error(request, "Passwords do not match.")
                return redirect('crud:index')
            
            
            if len(password) < 8:
                messages.error(request, "Password should be at least 8 characters.")
                return redirect('crud:index')

            new_registration = Registration(username=username, email=email, password=password)
            new_registration.save()
            messages.success(request, "Registration successful!")
            return redirect('crud:index')
        else:
            error_messages = form.errors
            for field, error in error_messages.items():
                messages.error(request, f"{field}: {error}")
            return redirect('crud:reg')
    else:
        form = RegisterForm()

    return render(request, 'register/reg.html', {'form': form})



def table (request):
    tasks = Task.objects.all()
    
    return render(request,'table/table.html', {'tasks': tasks})


def task(request):
    tasks = Task.objects.all()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data['task_name']
            description = form.cleaned_data['description']
            priority = form.cleaned_data['priority']
            assignee = form.cleaned_data['assignee']
            completion_status = form.cleaned_data['completion_status']
            
            task = Task(
                task_name=task_name,
                description=description,
                priority=priority,
                assignee=assignee,
                completion_status=completion_status
            )
            task.save()
            
            return redirect('crud:task')
    else:
        form = TaskForm()

    return render(request, 'table/task.html', {'form': form, 'tasks': tasks})

def update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('crud:table')
    else:
        form = TaskForm(instance=task)
    return render(request, 'table/task.html', {'form': form})


def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completion_status = not task.completion_status
    task.save()
    return redirect('crud:table')



def delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('crud:table')


def account(request):

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        form = LoginForm(request.POST)
        
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('crud:account')
        elif form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])  
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('crud:table')
                else:
                    return render(request, 'register/account.html', {'form': form})
            else:
                return render(request,  'register/account.html', {'form': form})
    else:
        user_form = UserRegistrationForm()
        form = LoginForm()
            
    return render(request, 'register/account.html', {'user_form': user_form, 'form': form})  



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    