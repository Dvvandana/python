from django.db import models
import re
import time, datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
FULL_NAME_REGEX = re.compile(r'^[A-Za-z]+[ ]+[A-Za-z]+$')

class UserManager(models.Manager):
    def basic_validator(self,formData):
        errors ={}
        if (len(formData['first_name'].strip()) < 2):
            errors["first_name"] = "First Name should be atleast 2 characters long"
        if (formData['first_name'].isalpha() == False):
            errors["first_name"] = "First Name should have alphabets"
        if (len(formData['last_name'].strip()) < 2):
            errors["last_name"] = "Last Name should be atleast 2 characters long"
        if (formData['last_name'].isalpha() == False):
            errors["last_name"] = "First Name should have alphabets"
        
        if not EMAIL_REGEX.match(formData['email']):
            errors['email'] = "Invalid Email Address"
        if (len(formData['password']) < 8):
            errors['password'] = "Password should ba atleast 8 characters long"
        if (formData['password'] != formData['confirm']):
            errors['confirm'] = "Please confirm the password" 

        #check for unique email address
        users = User.objects.filter(email = formData['email'])
        if len(users) > 0 :
            errors['unique_email'] = "Already existing email address"
        return errors

    def login_validator(self,formData):
        errors = {}
        if not EMAIL_REGEX.match(formData['email']):
            errors['email'] = "Invalid Email Address"
            return errors
        user = User.objects.filter(email = formData['email'])
        if len(user) <= 0:
            errors['email_validity'] = "Email is not Valid"
        else :
            cur_user = user[0]
            if bcrypt.checkpw(formData['password'].encode(),cur_user.password.encode()) == False:
                errors['password'] = "Password doesn't match for the email address"
        return errors

class TripManager(models.Manager):
    def trip_validator(self,formData):
        print("Inside validate")
        errors = {}
        if len(formData['destination'].strip()) < 3 :
            errors['destination'] = "Destination should be aleats 3 characters long"
        if len(formData['plan']) < 3 :
            errors['plan'] = "Plan should be aleats 3 characters long"
        
        if len(formData['start_date']) <= 0 :
            errors['start_date'] = "start_date cant be empty"
        if len(formData['end_date']) <= 0 :
            errors['end_date'] = "end_date cant be empty"
        try:
            given_start = datetime.datetime.strptime(formData['start_date'],"%Y-%m-%d")
            given_end = datetime.datetime.strptime(formData['end_date'],"%Y-%m-%d")
            cur_date = datetime.datetime.today()
            if given_start < cur_date :
                errors['start_date'] = "Start Date shgould be from future"
            else: 
                if (given_start > given_end):
                    errors['date'] = "End date should be more than start date"
        except:
            errors['date'] = "Please enter valid dates"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return f"{self.first_name}"

class Trip(models.Model):
    destination= models.CharField(max_length=45)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User,related_name = "created_trips")
    travellers = models.ManyToManyField(User,related_name = "trips_joined")
    objects = TripManager()

    def __repr__(self):
        return f"{self.destination} trip is created by {self.created_by.first_name}"