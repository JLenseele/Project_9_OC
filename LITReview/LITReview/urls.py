"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the included() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import review.views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', review.views.login_page, name='login'),
    path('signup/', review.views.signup, name='signup'),
    path('logout/', review.views.logout_user, name='logout'),

    path('flux/', review.views.flux, name='flux'),
    path('flux/ticket/', review.views.ticket_create, name='ticket-create'),
    path('flux/review/', review.views.review_create, name='review-create'),
    path('flux/review/<int:ticket_id>', review.views.review_create, name='review-from-ticket'),

    path('abo/', review.views.abo, name='abo'),
    path('abo/<int:sub_id>/unsub/', review.views.unsub, name='unsub'),

    path('mypost/', review.views.mypost, name='mypost'),
    path('mypost/<int:post_id>/<str:post_type>/change/', review.views.mypost_change, name='mypost-change'),
    path('mypost/<int:post_id>/<str:post_type>/delete/', review.views.mypost_delete, name='mypost-delete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
