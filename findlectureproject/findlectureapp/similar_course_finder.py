from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Sample course descriptions
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
