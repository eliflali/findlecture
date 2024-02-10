# scraper/scraping.py
import requests
from bs4 import BeautifulSoup
import pickle
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import Course  # Adjust the import path as necessary

# Function to remove cookies
def remove_cookies():
    # The following lines attempt to delete the cookies file if it exists
    # This is an approximation of the PHP version's file_put_contents("/tmp/cok", "");
    # Please note that Python's requests library handles cookies differently, and this may not be necessary
    cookies_file = "/tmp/cok"
    if os.path.exists(cookies_file):
        os.remove(cookies_file)

    pom_file = "/tmp/pom"
    if os.path.exists(pom_file):
        os.remove(pom_file)

# Function that emulates the curl_url_with_vars function in PHP
def python_request_with_vars(url, vars, persistent=False, session=None):
    if not persistent or session is None:
        session = requests.Session()
        # requests handles cookies automatically; there's no need for a cookie jar file
        session.verify = False  # Similar to CURLOPT_SSL_VERIFYPEER in PHP

    response = session.post(url, data=vars)

    if not persistent:
        session.close()

    return response.text

def parse_courses(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    # Use BeautifulSoup to find the courses in the HTML
    # This is a placeholder: you'll need to tailor this to the actual structure of the HTML
    courses = []
    for course_html in soup.find_all('table'):
        # Extract the relevant information from each course element
        # e.g., course_name = course_html.find('some_inner_selector').text
        courses.append(course_name)
    return courses

# Function to handle cookie management
def manage_cookies(session, save=True):
    if save:
        # Save cookies to a file
        with open('/tmp/cookies', 'wb') as f:
            pickle.dump(session.cookies, f)
    else:
        # Load cookies from a file
        with open('/tmp/cookies', 'rb') as f:
            session.cookies.update(pickle.load(f))

def get_course_names():
    session = requests.Session()
    session.verify = False  # Similar to CURLOPT_SSL_VERIFYPEER in PHP

    # First request to get cookies
    url = 'https://oibs.metu.edu.tr/cgi-bin/View_Program_Details_58/View_Program_Details_58.cgi'
    #url = 'https://oibs2.metu.edu.tr/View_Program_Course_Details_64/main.php'
    vars = {'SubmitName': 'Submit', 'SaFormName': 'action_index__Findex_html'}
    response = session.post(url, data=vars)
    manage_cookies(session, save=True)

    # Load HTML and parse
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all("table")
    
    data_table = tables[2]  # Adjust index based on your needs
    all_tables_data = []
    result_tables = {}
    for table in tables:
        table_data = {}
        rows = table.find_all('tr')
        i=0
        for row in rows:
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            if(len(row_data )>2):
                table_data[row_data[1]]=row_data[2:]
            i+=1
        all_tables_data.append(table_data)

    return {"tables": all_tables_data}

def similar_course_finder():
    courses = [
    ["CRP454", "URBAN TRANSPORT SYSTEMS: PLANNING AND DESIGN", "3", "3", "0", "5.0", "Planning and design of transport networks, modes, systems, stations. Network and urban form considerations. Route and capacity planning for public transport systems. Planning pedestrian circulation, principles of city center pedestrianisation. New Urbanism movement and planning for pedestrian-oriented and transit-oriented neighbourhoods. Principles of traffic calming. Design considerations for planning car parks, road junctions, stations, and interchange facilities."]
    # Add more courses as needed
    ]

    # Extract descriptions
    descriptions = [course[-1] for course in courses]

    # Vectorize descriptions
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(descriptions)

    # Example query
    query = ["Design considerations for urban transport and pedestrian-friendly spaces."]
    query_tfidf = vectorizer.transform(query)

    # Calculate similarity
    similarity_scores = cosine_similarity(query_tfidf, tfidf_matrix)

    # Find the most similar course
    most_similar_course_index = np.argmax(similarity_scores)
    most_similar_course = courses[most_similar_course_index]

    print("Most similar course based on description:", most_similar_course[0], "-", most_similar_course[1])
    return {"data": most_similar_course[0] + "-" + most_similar_course[1]} 

def get_course_contents(course_link, session):
    vars = {'SubmitName': 'Submit', 'SaFormName': 'action_index__Findex_html'}
    course_response = session.post(course_link, data=vars)
    manage_cookies(session, save=True)

    # Load HTML and parse
    soup = BeautifulSoup(course_response.content, 'html.parser')
    h3_tags = soup.find_all('h3')

    for h3 in h3_tags:
        # Use .next_sibling to get the content immediately following each <h3> tag
        following_content = h3.next_sibling
        
        # Since .next_sibling might return a NavigableString or another tag,
        # we check if it's not a tag before printing
        if following_content and not following_content.name:
            return following_content.strip()


def scrape_website():
    session = requests.Session()
    session.verify = False  # Similar to CURLOPT_SSL_VERIFYPEER in PHP

    department_data = get_course_names()
    departments = department_data["tables"][2]

    all_tables_data = []
    for department in departments:
        if len(department) == 3:
            url = 'https://catalog.metu.edu.tr/prog_courses.php?prog=' + department
            vars = {'SubmitName': 'Submit', 'SaFormName': 'action_index__Findex_html'}
            response = session.post(url, data=vars)
            manage_cookies(session, save=True)

            # Load HTML and parse
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all("table")

            
            for table in tables:
                table_data = []
                rows = table.find_all('tr')
                for row in rows:
                    row_data = [cell.get_text(strip=True) for cell in row.find_all(['td'])]
                    #print("row", row_data)
                    course_name = row_data[0]
                    print(course_name)
                    course_code = department + '0'
                    course_link = "https://catalog.metu.edu.tr/"
                    a_tag = row.find('a')
                    if a_tag:
                        # Extract the href attribute
                        course_link = course_link + a_tag.get('href')

                    
                    course_contents = get_course_contents(course_link, session)
                    if course_contents is None or course_name == "Course Code":
                        continue
                    # Create and save the course object
                    else:
                        Course.objects.create(
                            department=department,
                            course_name=course_name,
                            course_code=course_code,
                            course_link=course_link,
                            course_contents=course_contents
                        )

                    row_data.append(course_contents)

                    table_data.append(row_data)
                all_tables_data.append(table_data)
                # Write to a JSON file
                with open('course_data.json', 'w', encoding='utf-8') as f:
                    json.dump(all_tables_data, f, ensure_ascii=False, indent=4)

    raw_data = response.text

    return {"data": all_tables_data}
