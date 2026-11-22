from tempfile import template

from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = "skills"
urlpatterns = [
    # ex: /skills/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /skills/about
    path("about", views.AboutView.as_view(), name="about"),
    # ex: /skills/login
    path('login/', LoginView.as_view(template_name = "skills/login.html", next_page = "skills:index"), name='login'),
    # ex /skills/logout
    path("logout/", LogoutView.as_view(next_page="skills:index"), name="logout"),
    # ex: /skills/skill_add
    path("skill_add/", views.skill_create, name="skill_add"),
    # ex: /skills/skill_edit/1
    path("skill_edit/<int:pk>/", views.skill_create, name="skill_edit"),
    # ex: /skills/skill_detail/1
    path("skill_detail/<int:pk>/", views.skill_create, name="skill_detail"),
    # ex: /skills/activity_add
    path("activity_add/", views.skill_create, name="activity_add"),
    # ex: /skills/activity_edit/1
    path("activity_edit/<int:pk>/", views.skill_create, name="activity_edit"),
    # ex: /skills/offer_add
    path("offer_add/", views.skill_create, name="offer_add"),
    # ex: /skills/offer_edit/1
    path("offer_edit/<int:pk>/", views.skill_create, name="offer_edit"),
    # ex: /skills/request_add
    path("request_add/", views.skill_create, name="request_add"),
    # ex: /skills/request_edit/1
    path("request_edit/<int:pk>/", views.skill_create, name="request_edit"),
]