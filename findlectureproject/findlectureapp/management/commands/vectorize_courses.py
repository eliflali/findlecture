# management/commands/vectorize_courses.py
from django.core.management.base import BaseCommand
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

from findlectureapp.models import Course  # Import your Course model

class Command(BaseCommand):
    help = 'Vectorizes course descriptions and saves the model for later use.'

    def handle(self, *args, **options):
        # Fetch course descriptions from your database
        courses = Course.objects.all()
        descriptions = [course.course_contents for course in courses]

        # Vectorize descriptions
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(descriptions)

        # Save the vectorizer and matrix for later use
        with open('vectorizer.pkl', 'wb') as f:
            pickle.dump(vectorizer, f)
        with open('tfidf_matrix.pkl', 'wb') as f:
            pickle.dump(tfidf_matrix, f)

        self.stdout.write(self.style.SUCCESS('Successfully vectorized course descriptions.'))
