from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .scraping import scrape_website
# scraper/views.py
from django.http import JsonResponse
from .scraping import scrape_website
import requests
from bs4 import BeautifulSoup

def scrape_courses(request):
    url = "https://oibs2.metu.edu.tr/View_Program_Course_Details_64/main.php"
    
    # Initial GET request to fetch form options (if needed)
    initial_response = requests.get(url)
    initial_soup = BeautifulSoup(initial_response.text, 'html.parser')
    
    # Example of extracting department options; adjust according to actual HTML structure
    department_options = initial_soup.find('select', {'name': 'select_dept'}).find_all('option')
    departments = {opt.text: opt['value'] for opt in department_options if opt['value']}
    
    # Assuming 'Biology/Biyoloji' is a valid option; replace with a dynamic selection as needed
    selected_department_value = 'Biology/Biyoloji'
    
    # Proceed only if the department is found
    if selected_department_value:
        data = {
            "select_dept": selected_department_value,  # Use the value from the options
            "submit_CourseList": "Submit"
        }

        response = requests.post(url, data=data)
        raw_data = response.text

        if "Information about the department could not be found." in raw_data:
            context = {"error": "Information about the department could not be found."}
        else:
            # Pass the raw HTML response to the template
            context = {"raw_html": raw_data}
    else:
        context = {"error": raw_data}

    return render(request, 'courses.html', context)

def scrape_view(request):
    data = scrape_website()
    print("data", data)
    return render(request, 'template.html', data)


class ScrapeView(APIView):
    def get(self, request, format=None):
        data = scrape_website()
        return Response({"data": data})

