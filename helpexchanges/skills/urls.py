from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = "skills"
urlpatterns = [
    # ex: /skills/
    path("", views.FaqView.as_view(), name="index"),
    
]