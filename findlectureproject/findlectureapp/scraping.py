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
