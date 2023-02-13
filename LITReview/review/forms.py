from django import forms
from review.models import Ticket, Review, UserFollows
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import TextInput, EmailInput


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=63,
        label='Nom d’utilisateur',
        widget=forms.TextInput(
            attrs={'placeholder': "Nom d'utilisateur",
                   'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=63,
        label='Mot de passe',
        widget=forms.PasswordInput(
            attrs={'placeholder': "Mot de passe",
                   'class': 'form-control'})
    )


class SignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': "Nom d'utilisateur",
                   'class': 'form-control'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': "Mot de passe",
                   'class': 'form-control'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': "Confirmer votre Mot de passe",
                   'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = 'username', 'password1', 'password2'


class TicketForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Titre',
                                                          'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": '5',
                                                               'placeholder': 'Description',
                                                               'class': 'form-control'}))

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    headline = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Titre',
                                                             'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": '5',
                                                        'placeholder': 'Commentaire',
                                                        'class': 'form-control'}))

    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES,)

    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']


class FollowForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']

