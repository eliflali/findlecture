from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .scraping import scrape_website
# scraper/views.py
from django.http import JsonResponse
from .scraping import scrape_website
from .scraping import similar_course_finder
from .scraping import remove_cookies, python_request_with_vars
import requests
from bs4 import BeautifulSoup
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from findlectureapp.models import Course
"""
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

        # Fetch the corresponding course objects
        course_ids = [Course.objects.all()[index].id for index in top_indices]
        courses = Course.objects.filter(id__in=course_ids)
    else:
        courses = []

    return render(request, 'search.html', {'courses': courses, 'query': query})
"""
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
    
def scrape_courses(request):
    url = "https://catalog.metu.edu.tr/prog_courses.php?prog=567"

    # Assuming you want to start with a clean session each time
    with requests.Session() as session:
        # If you need to fetch initial form options, you can do so here
        # For simplicity, this step is skipped as it seems you already know the form data to submit

        # Form data to submit
        form_data = {
            'select_dept': '874',  # Example department
            'select_semester': '20183',  # Example semester
            'submit_CourseList': 'Submit',
            'textWithoutThesis': '1',
            'hidden_redir': 'Login'  # Assuming this is needed based on your initial code
        }

        # Submit the form
        response = session.post(url, data=form_data)
        print(response.text)
        # Check for specific error message in response
        if "Information about the department could not be found." in response.text:
            context = {"error": "Information about the department could not be found."}
        else:
            # If no error, pass the raw HTML response to the template
            # You might want to parse the response with BeautifulSoup if you need to extract specific data
            context = {"raw_html": response.text}

    return render(request, 'courses.html', context)

def scrape_view(request):
    data = scrape_website()
    #print("data", data)
    #print(data)
    tables = data
    return render(request, 'template.html', tables)

def similar_courses(request):
    data = similar_course_finder()
    #print("data", data)
    #print(data)
    tables = data
    return render(request, 'template.html', tables)


class ScrapeView(APIView):
    def get(self, request, format=None):
        data = scrape_website()
        return Response({"data": data})

