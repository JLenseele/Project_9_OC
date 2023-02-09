from django import forms
from review.models import Ticket, Review, UserFollows


class LoginForm(forms.Form):

    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']


class FollowForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']

