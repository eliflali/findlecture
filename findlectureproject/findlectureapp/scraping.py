# scraper/scraping.py
import requests
from bs4 import BeautifulSoup
import pickle
import json
import os

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
    #print(data_table)
    all_tables_data = []
    result_tables = {}
    for table in tables:
        #print(table)
        table_data = {}
        rows = table.find_all('tr')
        i=0
        for row in rows:
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            #print("a",row_data)
            if(len(row_data )>2):
                table_data[row_data[1]]=row_data[2:]
            i+=1
        all_tables_data.append(table_data)
        #print(table_data[0])

    return {"tables": all_tables_data}

    #return {"data": str(soup)}

def scrape_website():
    session = requests.Session()
    session.verify = False  # Similar to CURLOPT_SSL_VERIFYPEER in PHP

    # First request to get cookies
    #url = 'https://oibs.metu.edu.tr/cgi-bin/View_Program_Details_58/View_Program_Details_58.cgi'
    #url = 'https://oibs2.metu.edu.tr/View_Program_Course_Details_64/main.php'
    
    # Get the course names
    course_data = get_course_names()
    courses = course_data["tables"][2]

    for course in courses:
        print(course)
    url = 'https://catalog.metu.edu.tr/prog_courses.php?prog=567'
    vars = {'SubmitName': 'Submit', 'SaFormName': 'action_index__Findex_html'}
    response = session.post(url, data=vars)
    manage_cookies(session, save=True)

    # Load HTML and parse
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all("table")
    
    #data_table = tables[2]  # Adjust index based on your needs

    all_tables_data = []
    for table in tables:
        table_data = []
        rows = table.find_all('tr')
        for row in rows:
            
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['td'])]
            #print("row", row_data)
            table_data.append(row_data)
        all_tables_data.append(table_data)

    # Write to a JSON file
    with open('course_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_tables_data, f, ensure_ascii=False, indent=4)

    #print(response)
    raw_data = response.text
    #print(raw_data)

    return {"data": all_tables_data}
