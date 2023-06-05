from django.urls import path

from . import views

app_name = 'verb'

urlpatterns = [
    path('', views.index, name='index'),
    path('search-sentences/', views.search_sentences, name='search_sentences'),


]
