from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db.models import CharField, Value, Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from review.forms import TicketForm, ReviewForm, FollowForm, SignupForm
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
                return redirect('flux')
            else:
                message = 'Identifiants invalides.'
    return render(request, 'review/login.html', context={'form': form, 'message': message})


def logout_user(request):
    logout(request)
    return redirect('login')


def signup(request):
    form = SignupForm()
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
        Q(user__followed_by__user=request.user) ^
        Q(user=request.user)
    ).distinct()

    tickets_filter = Ticket.objects.filter(user=request.user)

    reviews = Review.objects.filter(
        Q(user__followed_by__user=request.user) ^
        Q(user=request.user) ^
        Q(ticket__in=tickets_filter)
    ).distinct()

    liste = []
    tickets_review = Review.objects.values('ticket')
    for tick in tickets_review:
        liste.append(tick['ticket'])

    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    print(reviews)
    print(tickets)
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True)

    return render(request, 'review/flux.html', context={'posts': posts, 'liste': liste})


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

    message = ''

    subscriber = UserFollows.objects.filter(followed_user=request.user)
    subscription = UserFollows.objects.filter(user=request.user)
    print(subscription)
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            abo = form.cleaned_data['followed_user']
            try:
                userfollow = User.objects.get(username=abo)
                if userfollow == request.user:
                    message = "Vous ne pouvez pas suivre votre propre compte"
                else:
                    follow = UserFollows()
                    follow.user = request.user
                    follow.followed_user = userfollow
                    follow.save()

            except ObjectDoesNotExist:
                message = "Cet utilisateur n'existe pas"
            except IntegrityError:
                message = "Vous suivez déja cet utilisateur"
    else:
        form = FollowForm()

    return render(request, 'review/abo.html',
                  context={
                      'form': form,
                      'subscriber': subscriber,
                      'subscription': subscription,
                      'message': message
                  })


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
                  context={
                      'posts': posts
                  })


@login_required
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


def error_404_view(request, exception):
    return render(request, '404.html')
