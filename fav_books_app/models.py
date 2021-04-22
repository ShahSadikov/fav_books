from django.db import models
from datetime import datetime
from datetime import timedelta
import re
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        #names_____________________________
        if len(postData['first_name']) < 2:
            errors["first_name"] = "The first name must be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "The last name must be at least 2 characters."

        #check if the age > 13_______________ 
        today = datetime.today()
        eligible_age = today - timedelta(days=365*13)
        print(eligible_age)
        if len(postData['dob']) == 0:
            errors['enter_dob'] = "The date of birth must be entered."
        elif postData['dob'] > str(eligible_age): # CHECK THIS LOGIC!!! NOT SURE IF IT'S WORKING CORRECTLY
            errors['not_eligible'] = "Your age is not valid. Try again next year."

        #email______________________________
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "The valid email address must be entered."
        # #unique email check:
        current_user = User.objects.filter(email=postData['email'])
        if len(current_user) >= 1:
            errors['duplicate'] = "The email is already in use." 
        #password___________________________
        if len(postData['password']) < 8:
            errors["password"] = "The password must be at least 8 characters long."
        #password match:
        if postData['password'] != postData['confirm_password']:
            errors["mismatch"] = "The passwords must match!"
        
        return errors

    def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) == 0:
            errors['wrong_user'] = "Enter a valid email or password."
        #email check:
        elif len(postData['email']) == 0:
            errors['email'] = "You must enter an email."
        #password check:
        elif len(postData['password']) == 0:
            errors['password'] = "You must enter a password."
        elif len(postData['password']) < 8:
            errors['password'] = "The password isn't long enough."
        #check if the email is in DB
        # if so check to see if the email/password match
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors["password"] = "Email and password do not match."
            
        return errors

#User model:
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    dob = models.DateTimeField()
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #books_uploaded_by = a list of books uploaded by a given user
    #books_liked_by = a list of books that are liked by a given user

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}

        if len(postData['title']) == 0:
            errors['title'] = "Enter a book title."
        if len(postData['description']) < 5:
            errors['description'] = "Description must be at least 5 characters long."

        return errors
#Books
class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #RELATIONSHIP__________________________________________________________
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded_by", on_delete=models.CASCADE)
        #the user who uploaded a given book
    books_liked_by = models.ManyToManyField(User, related_name="user_who_liked")
        #the list of users that liked a given book
    
    objects = BookManager()
    
