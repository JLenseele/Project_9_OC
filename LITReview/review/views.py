from . import forms

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from django.shortcuts import render, redirect

from django.db.models import CharField, Value, Q
from django.db import IntegrityError

from itertools import chain

from review.forms import TicketForm, ReviewForm, FollowForm, SignupForm
from review.models import Ticket, Review, UserFollows

import random


def login_page(request):
    """
    Fonction permettant de récupérer le formulaire forms.LoginForm()
    et de s'authentifier'
    """
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
    """
        Fonction permettant de déconnecter l'utilisateur actif
    """
    logout(request)
    return redirect('login')


def signup(request):
    """
        Fonction de création d'un nouvel utilisateur
        form : username / password / confirm password
    """
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
    """
        Fonction qui récupère les posts (tickets / reviews) lié à l'user:
        - créé par l'user authentifié
        - créé par un user suivi par l'user authentifié
        - en réponse à un ticket de l'user authentifié
        -> trié par ordre inverse de création (time_created)
    """
    tickets = Ticket.objects.filter(
        # ticket créé par user follow
        Q(user__followed_by__user=request.user) |
        # ticket créé par user actif
        Q(user=request.user)
    ).distinct()

    # liste des tickets créés par user actif
    tickets_filter = Ticket.objects.filter(user=request.user)

    reviews = Review.objects.filter(
        # review créé par user follow
        Q(user__followed_by__user=request.user) |
        # review créé par user actif
        Q(user=request.user) |
        # review créé en réponse à un ticket de l'user actif
        Q(ticket__in=tickets_filter)
    ).distinct()

    liste = []
    tickets_review = Review.objects.values('ticket')
    for tick in tickets_review:
        liste.append(tick['ticket'])

    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'review/flux.html', context={'posts': posts,
                                                        'liste': liste,
                                                        'page_obj': page_obj})


@login_required
def ticket_create(request):
    """
        Fonction de creation de nouveaux tickets
        GET -> formulaire
        POST -> recup data -> save()
    """
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
    """
        Fonction de creation de nouvelles reviews
        GET -> formulaire
        POST -> recup data -> save()
    """
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
    """
        Fonction de creation de lien
        type 'follow' entre deux users
    """

    message = ''

    subscriber = UserFollows.objects.filter(followed_user=request.user)
    subscription = UserFollows.objects.filter(user=request.user)

    sub_name = UserFollows.objects.filter(user=request.user).values_list('followed_user',
                                                                         flat=True)
    suggestions = User.objects.filter(
        ~Q(username=request.user) &
        ~Q(id__in=sub_name)
    ).distinct()

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
                message = "Vous suivez deja cet utilisateur"
    else:
        form = FollowForm()

    return render(request, 'review/abo.html',
                  context={'form': form,
                           'subscriber': subscriber,
                           'subscription': subscription,
                           'message': message,
                           'suggestions': suggestions}
                  )


@login_required
def unsub(request, sub_id):
    """
        Fonction suppression de lien
        type 'follow" entre deux users
    """
    sub = UserFollows.objects.get(id=sub_id)
    sub.delete()
    return redirect('abo')


@login_required
def mypost(request):
    """
        Fonction de récupération des posts créés
        par l'user authentifié
    """
    ticket = Ticket.objects.filter(user=request.user)
    review = Review.objects.filter(user=request.user)

    review = review.annotate(content_type=Value('REVIEW', CharField()))
    ticket = ticket.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        chain(review, ticket),
        key=lambda post: post.time_created,
        reverse=True)
    return render(request, 'review/post.html',
                  context={'posts': posts}
                  )


@login_required
def mypost_change(request, post_id, post_type):
    """
        Fonction de modification de posts (ticket ou review)
        créés par l'utilisateur
    """
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
    """
        Fonction de suppression de posts (ticket ou review)
        créés par l'utilisateur
    """
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
