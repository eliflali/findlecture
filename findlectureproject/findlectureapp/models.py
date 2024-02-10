from django.db import models

class Course(models.Model):
    department = models.CharField(max_length=100)
    course_name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=20)
    course_link = models.URLField(max_length=200)
    course_contents = models.TextField()

    def __str__(self):
        return self.course_name
