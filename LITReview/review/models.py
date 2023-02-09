from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048,
                                   blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ImageField(null=True,
                              blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192,
                            blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(to=Ticket,
                               on_delete=models.CASCADE,
                               related_name='with_ticket')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                          MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following')
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')
