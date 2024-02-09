from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .scraping import scrape_website
# scraper/views.py
from django.http import JsonResponse
from .scraping import scrape_website
from .scraping import remove_cookies, python_request_with_vars
import requests
from bs4 import BeautifulSoup
import os

"""
def scrape_courses(request):
    url = "https://oibs2.metu.edu.tr/View_Program_Course_Details_64/main.php"
    vars = {'SubmitName':'Submit','SaFormName':'action_index__Findex_html'}
    # Initial GET request to fetch form options (if needed)
    initial_response = python_request_with_vars(url, vars)
    initial_soup = BeautifulSoup(initial_response, 'html.parser')
    
    # Proceed only if the department is found
    #if selected_department_value:
    
    vars ={
    'select_dept' : '874',
    'select_semester' : '20183',
    "submit_CourseList": "Submit",
    "textWithoutThesis": "1",
    "hidden_redir": "Login"
    } 
    

    remove_cookies()

    raw_data = python_request_with_vars(url, vars)

    print(raw_data)

    if "Information about the department could not be found." in raw_data:
        
        context = {"error": "Information about the department could not be found."}
    else:
        # Pass the raw HTML response to the template
        context = {"raw_html": raw_data}


    return render(request, 'courses.html', context)
"""
"""
def scrape_courses(request):
    url = "https://oibs2.metu.edu.tr/View_Program_Course_Details_64/main.php"

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
"""

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


class ScrapeView(APIView):
    def get(self, request, format=None):
        data = scrape_website()
        return Response({"data": data})

