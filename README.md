# METU Course Finder

The METU Course Finder is a Django-based web application designed to simplify the process of selecting courses for students at Middle East Technical University (METU). By leveraging advanced semantic search capabilities, the application allows students to discover courses that not only match their academic requirements but also align with their personal interests and career aspirations.

## Features

* #### Semantic Course Search:
Utilizes NLP (Natural Language Processing) techniques to understand the context and semantics behind search queries, providing more relevant search results based on course descriptions and content.
* #### User-Friendly Interface:
A clean and modern UI/UX that makes it easy for students to navigate through the application and find the information they need quickly.
* #### Course Details: 
Access detailed information about each course, including descriptions, credits, and direct links to official METU course pages.
* #### Responsive Design: 
Ensures a seamless experience across various devices and screen sizes, enabling students to access the application anytime, anywhere.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Before you begin, ensure you have the following installed:

* Python (3.8 or newer)
* Django (3.2 or newer)

### Installation

1. Clone the repository:
   ```
   git clone  https://github.com/eliflali/findlecture.git
   ```
   
2. Navigate to the project directory:
   ```cd findlectureproject```
3. Run the development server:
   ``` python manage.py runserver ``` 
4. Open your browser and navigate to http://127.0.0.1:8000/ to see the application in action.

## How It Works

The core functionality of the METU Course Finder application revolves around providing an intuitive and efficient way for students to discover courses that align with their interests and academic goals. This is achieved through a combination of web scraping, data storage, and advanced semantic search capabilities. Below is an overview of the key components and technologies involved in the application:

### Course Data Collection
* #### Web Scraping:
The application begins by collecting course data from the official METU website. This process involves programmatically navigating the site, extracting relevant course information such as course names, codes, descriptions, and links to detailed pages. This data is then stored in a database for easy retrieval and search.

* #### Database Storage: 
After scraping, course information is saved into a Django model (Course), which includes fields for the course name, code, description, and link. Django's ORM (Object-Relational Mapping) facilitates interaction with the database, allowing for efficient data manipulation and retrieval.
Semantic Search Implementation

* ####  TF-IDF Vectorization:
The application uses the Term Frequency-Inverse Document Frequency (TF-IDF) method to convert course descriptions into a numerical format (vectors) that can be processed by search algorithms. TF-IDF helps highlight the importance of words within each course description relative to the entire dataset, making it easier to identify relevant courses based on search queries.

* #### Cosine Similarity:
To determine the relevance of each course to a given search query, the application calculates the cosine similarity between the TF-IDF vector of the query and the vectors of all course descriptions. This measure of similarity helps identify courses whose descriptions are most closely aligned with the user's search terms.

* #### Indexing and Retrieval: 
Courses are indexed based on their descriptions' TF-IDF vectors, allowing for quick retrieval of the most relevant courses when a search query is made. The search functionality sorts courses by their similarity scores, ensuring that the most semantically related courses are presented to the user.

### User Interaction
* #### Search Interface:
Users interact with the application through a simple and intuitive search interface, where they can enter keywords or phrases related to their interests. The application then displays a list of courses that match the search criteria, ranked by relevance.

* #### Course Details: 
For each course in the search results, users can view basic information such as the course name and description. Additionally, a link is provided to the official METU course page for detailed information, allowing students to explore the course further.

### Technologies Used
* Django: Serves as the application's web framework, handling routing, models, views, and templates.
* Scikit-learn: A machine learning library used for TF-IDF vectorization and calculating cosine similarity, central to the semantic search functionality.
* Python: The primary programming language for the application, used for web scraping, data processing, and implementing the search algorithm.
* SQLite/PostgreSQL: Depending on the deployment, Django's default SQLite database or a more scalable option like PostgreSQL can be used for data storage.


https://github.com/eliflali/findlecture/assets/63200204/1f1fe1de-5a61-4de8-a06b-3bb4ab349cc7

