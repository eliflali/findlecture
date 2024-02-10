# scraper/urls.py
from django.urls import path
from .views import scrape_view
from .views import search_courses

urlpatterns = [
    path('scrape/', scrape_view, name='scrape'),
    path('', search_courses, name='search_courses'),
]
