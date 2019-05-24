from django.db import models
import datetime
from apps.login.models import *

class MovieManager(models.Manager):
    def validate(self, form):
        errors = {}

        if len(form['title']) < 1:
            errors['title'] = "Please enter title"
        
        if len(form['year']) < 1:
            errors['year'] = "Please enter release year"
        elif int(form['year']) < 1888:
            errors['year'] = "Too old, movies were not made before 1888"
        elif int(form['year']) > datetime.now().year:
            errors['year'] = "Unreleased movies are not allowed"

        return errors

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, models.CASCADE, "movies_added")
    favorited_by = models.ManyToManyField(User, "favorites")
    objects = MovieManager()


    def __repr__(self):
        return f"<Movie object: {self.title} ({self.year})>"