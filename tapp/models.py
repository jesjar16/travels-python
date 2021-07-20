from django.db import models
from datetime import datetime, timedelta
from calendar import isleap
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking name
        if len(postData['name']) == 0:
            errors['name_emp'] = "Name can not be empty"
        elif len(postData['name']) > 0 and len(postData['name']) < 3:
            errors['name_len'] = "Name should be less at least 3 characters long"
            
        # checking username
        if len(postData['username']) == 0:
            errors['username_emp'] = "Username can not be empty"
        elif len(postData['username']) > 0 and len(postData['username']) < 3:
            errors['username_len'] = "Username should be less at least 3 characters long"
        
        # checking password    
        if len(postData['password']) == 0:
            errors['password_emp'] = "Password can not be empty"
        elif len(postData['password']) < 8:
            errors['password_len'] = "Password should be less at least 8 characters long"                
        
        # checking password 2   
        if len(postData['password2']) == 0:
            errors['password2_emp'] = "Password confirmation can not be empty"
        elif len(postData['password2']) < 8:
            errors['password2_len'] = "Password confirmation should be less at least 8 characters long"    
            
        # checking password 1 and 2
        if len(postData['password']) > 7 and len(postData['password2']) > 7:
            if postData['password'] != postData['password2']:    
                errors['password_dif'] = "Passwords do not match, please try again"

        return errors
    
    def basic_validator2(self, postData):

        # errors dictionnary
        errors = {}
        
       # checking username
        if len(postData['username_login']) == 0:
            errors['username_login_emp'] = "Username can not be empty"
        elif len(postData['username_login']) > 0 and len(postData['username_login']) < 3:
            errors['username_login_len'] = "Username should be less at least 3 characters long"
                
        # checking password    
        if len(postData['password_login']) == 0:
            errors['password_login_emp'] = "Password can not be empty"
        elif len(postData['password_login']) < 8:
            errors['password_login_len'] = "Password should be less at least 8 characters long"
        
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # planner = user who created the plan
    # joiners = users who joined the trip
    objects = UserManager()

    def __repr__(self):
        return f"User: (ID: {self.id}) -> {self.name} {self.username}"

# new models for travel app
    
class TripManager(models.Manager):
    def basic_validator(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking trip
        if len(postData['destination']) == 0:
            errors['destination_emp'] = "Destination can not be empty!"
            
        if len(postData['description']) == 0:
            errors['description_emp'] = "Description can not be empty!"     
            
        if len(postData['date_from']) == 0:
            errors['date_from_emp'] = "Travel Date From can not be empty!"       
            
        if len(postData['date_to']) == 0:
            errors['date_to_emp'] = "Travel Date To can not be empty!"                                        
                    
        if len(postData['date_from']) != 0 and len(postData['date_to']) != 0:                    
            # The strptime() method creates a datetime object from the given string.            
            date_from = datetime.strptime(postData['date_from'], "%Y-%m-%d")
            date_to = datetime.strptime(postData['date_to'], "%Y-%m-%d")
            today_date = datetime.today()
                
            # checking that date_to is greater than date_from    
            if date_from > date_to:
                errors['date_diff'] = "Travel date from should be less than Travel date to!"
                
            # checking dates are greater than today
            if date_from < today_date or date_to < today_date:
                errors['date_today_diff'] = "Both dates should be greater than today!"            
            
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_date_from = models.DateField()
    travel_date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    planned_by = models.ForeignKey(User, related_name="planner", on_delete=models.CASCADE) # the user who planned the trip
    user_who_join = models.ManyToManyField(User, related_name="joiners") # a list of users who joined the trip
    objects = TripManager()

    def __repr__(self):
        return f"Trip: (ID: {self.id}) -> {self.description}"