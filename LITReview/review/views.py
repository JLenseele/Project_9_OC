from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db.models import CharField, Value, Q

from review.forms import TicketForm, ReviewForm, FollowForm
from review.models import Ticket, Review, UserFollows

from itertools import chain


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
    tickets = Ticket.objects.filter(
        Q(user__followed_by__user=request.user) | Q(user=request.user)
    )
    reviews = Review.objects.filter(
        Q(user__followed_by__user=request.user) | Q(user=request.user)
    )
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True)
    return render(request, 'review/flux.html', {'posts': posts})


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
def review_create(request, ticket_id=None):
    if ticket_id is None:
        form_r = ReviewForm()
        form_t = TicketForm()
        if request.method == 'POST':
            form_r = ReviewForm(request.POST)
            form_t = TicketForm(request.POST, request.FILES)
            if all([form_r.is_valid(), form_t.is_valid()]):
                review = form_r.save(commit=False)
                ticket = form_t.save(commit=False)
                review.user = request.user
                ticket.user = request.user
                ticket.save()
                review.ticket = ticket
                review.save()
                return redirect('flux')
        context = {'form_review': form_r, 'form_ticket': form_t}
    else:
        form_r = ReviewForm()
        ticket = Ticket.objects.get(id=ticket_id)
        if request.method == 'POST':
            form_r = ReviewForm(request.POST)
            if form_r.is_valid():
                review = form_r.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                return redirect('flux')
        context = {'form_review': form_r, 'ticket': ticket}
    return render(request, 'review/review-create.html', context=context)


@login_required
def abo(request):
    form = FollowForm()
    subscriber = UserFollows.objects.filter(followed_user=request.user)
    subscription = UserFollows.objects.filter(user=request.user)
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            follow = form.save(commit=False)
            follow.user = request.user
            follow.save()
    return render(request, 'review/abo.html',
                  context=
                  {'form': form, 'subscriber': subscriber, 'subscription': subscription})


@login_required
def unsub(request, sub_id):
    sub = UserFollows.objects.get(id=sub_id)
    sub.delete()
    return redirect('abo')


@login_required
def mypost(request):
    ticket = Ticket.objects.filter(user=request.user)
    review = Review.objects.filter(user=request.user)

    review = review.annotate(content_type=Value('REVIEW', CharField()))
    ticket = ticket.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        chain(review, ticket),
        key=lambda post: post.time_created,
        reverse=True)
    return render(request, 'review/post.html',
                  context=
                  {'posts': posts})


def mypost_change(request, post_id, post_type):
    if post_type == 'TICKET':
        ticket = Ticket.objects.get(id=post_id)
        if request.method == 'POST':
            form = TicketForm(request.POST, instance=ticket)
            if form.is_valid:
                form.save()
                return redirect('mypost')
        else:
            form = TicketForm(instance=ticket)
    else:
        review = Review.objects.get(id=post_id)
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid:
                form.save()
                return redirect('mypost')
        else:
            form = ReviewForm(instance=review)
    return render(request, 'review/change-post.html', context={'form': form})


def mypost_delete(request, post_id, post_type):
    if post_type == 'TICKET':
        post = Ticket.objects.get(id=post_id)
        if request.method == 'POST':
            post.delete()
            return redirect('mypost')
    else:
        post = Review.objects.get(id=post_id)
        if request.method == 'POST':
            post.delete()
            return redirect('mypost')

    return render(request, 'review/delete-post.html', context={'post': post})
