from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.article, name="article"),
    path("search/", views.search, name="search"),
    path("create/", views.create_entry, name="create"),
    path("edit/<str:title>", views.edit_entry, name="edit"),
    path("random/", views.random_article, name="random"),
]
