from django.db import models
import re
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def validator(self, form):
        errors = {}

        if len(form['username']) < 1:
            errors['username'] = "Username cannot be blank"
        elif len(form['username']) < 2:
            errors['username'] = "Username should be at least 2 characters"   

        if len(form['email']) < 1:
            errors['email'] = "Email cannot be blank"
        elif not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Email is not valid!"
        else:
            result = User.objects.filter(email=form['email'])
            if len(result) > 0:
                errors['email'] = "Email is already registered"
        
        if len(form['password']) < 1:
            errors['password'] = "Password cannot be blank"
        elif len(form['password']) < 8:
            errors['password'] = "Passwords must be at least 8 characters"
        elif form['password'] != form['confirm_password']:
            errors['confirm_password'] = "Passwords do not match"
        
        if len(form['birthday']) < 1:
            errors['birthday'] = "Please enter your birthday"
        elif datetime.strptime(form['birthday'], '%Y-%m-%d') > datetime.today():
            errors['birthday'] = "New user cannot be from the future"

        return errors

class User(models.Model):
    username = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=70)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"<User object: {self.username} ({self.email} - {self.birthday})>"