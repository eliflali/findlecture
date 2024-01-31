# scraper/urls.py
from django.urls import path
from .views import scrape_view
from .views import scrape_courses

urlpatterns = [
    path('scrape/', scrape_view, name='scrape'),
    path('scrape_courses/', scrape_courses, name='scrape_courses'),
]
