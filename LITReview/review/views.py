from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from review.forms import TicketForm, ReviewForm
from review.models import Ticket, Review


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = {user.username}
            else:
                message = 'Identifiants invalides.'
    return render(request, 'review/login.html', context={'form': form, 'message': message})


def logout_user(request):
    logout(request)
    return redirect('login')


def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'review/signup.html', context={'form': form})


@login_required
def flux(request):
    tickets = Ticket.objects.all()
    return render(request, 'review/flux.html', {'tickets': tickets})


@login_required
def ticket_create(request):
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    return render(request, 'review/ticket-create.html', context={'form': form})


@login_required
def review_create(request):
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flux')
    return render(request, 'review/review-create.html', context={'form': form})


@login_required
def abo(request):
    return render(request, 'review/abo.html')


@login_required
def post(request):
    return render(request, 'review/post.html')
