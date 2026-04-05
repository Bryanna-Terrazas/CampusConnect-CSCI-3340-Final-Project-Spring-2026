from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Task, Event
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html', {})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out!")
    return redirect("login")


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, "profile.html", {"u_form": u_form, "p_form": p_form})


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            due_date=due_date or None
        )
        messages.success(request, 'Task created!')
        return redirect('task_list')
    return render(request, 'task_create.html')


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date') or None
        task.completed = 'completed' in request.POST
        task.save()
        messages.success(request, 'Task updated!')
        return redirect('task_list')
    return render(request, 'task_edit.html', {'task': task})


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted!')
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})


@login_required
def event_list(request):
    events = Event.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'events.html', {'events': events})


@login_required
def event_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        date = request.POST.get('date')
        category = request.POST.get('category')
        Event.objects.create(
            user=request.user,
            title=title,
            description=description,
            location=location,
            date=date or None,
            category=category
        )
        messages.success(request, 'Event created!')
        return redirect('event_list')
    return render(request, 'event_create.html')


@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.location = request.POST.get('location')
        event.date = request.POST.get('date') or None
        event.category = request.POST.get('category')
        event.save()
        messages.success(request, 'Event updated!')
        return redirect('event_list')
    return render(request, 'event_edit.html', {'event': event})


@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted!')
        return redirect('event_list')
    return render(request, 'event_confirm_delete.html', {'event': event})
