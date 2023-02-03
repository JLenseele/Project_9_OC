from django.shortcuts import render
from django.http import HttpResponse


def accueil(request):
    return HttpResponse('<h1> test </h1>')
