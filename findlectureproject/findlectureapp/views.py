from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .scraping import scrape_website
import requests
from bs4 import BeautifulSoup
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from findlectureapp.models import Course

def search_courses(request):
    query = request.GET.get('query', '')

    if query:
        # Load the precomputed vectorizer and TF-IDF matrix
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        with open('tfidf_matrix.pkl', 'rb') as f:
            tfidf_matrix = pickle.load(f)

        # Vectorize the query
        query_vector = vectorizer.transform([query])

        # Calculate similarity scores
        similarity_scores = cosine_similarity(query_vector, tfidf_matrix)

        # Find the most similar courses
        most_similar_indices = np.argsort(similarity_scores[0])[::-1]
        top_indices = most_similar_indices[:10]  # Adjust the number of results as needed

        # Assuming you have a way to map indices back to course IDs, fetch courses
        # For demonstration, let's fetch all courses and then reorder them (not efficient for large datasets)
        all_courses = list(Course.objects.all())
        courses = [all_courses[i] for i in top_indices if i < len(all_courses)]
    else:
        courses = []

    return render(request, 'search.html', {'courses': courses, 'query': query})

def scrape_view(request):
    data = scrape_website()
    return render(request, 'template.html', data)


class ScrapeView(APIView):
    def get(self, request, format=None):
        data = scrape_website()
        return Response({"data": data})

