# scraper/scraping.py
import requests
from bs4 import BeautifulSoup
import pickle

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

def scrape_website():
    session = requests.Session()
    session.verify = False  # Similar to CURLOPT_SSL_VERIFYPEER in PHP

    # First request to get cookies
    #url = 'https://oibs.metu.edu.tr/cgi-bin/View_Program_Details_58/View_Program_Details_58.cgi'
    url = 'https://oibs2.metu.edu.tr/View_Program_Course_Details_64/main.php'
    vars = {'SubmitName': 'Submit', 'SaFormName': 'action_index__Findex_html'}
    response = session.post(url, data=vars)
    manage_cookies(session, save=True)

    # Load HTML and parse
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all("table")
    
    data_table = tables[2]  # Adjust index based on your needs

    all_tables_data = []
    for table in tables:
        table_data = []
        rows = table.find_all('tr')
        for row in rows:
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            table_data.append(row_data)
        all_tables_data.append(table_data)

    return {"tables": all_tables_data}

    #return {"data": str(soup)}
