from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserManager, Book
import bcrypt

def index(request):
    return render(request, 'index.html')

#Create/register a new user_________________________________
def register_user(request):
    if request.method == "POST":
        #validation before saving to DB
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/') 

        #hash the password
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()
        ).decode()
        
        #create user
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            dob = request.POST['dob'],
            email = request.POST['email'],
            password = hashed_pw
        ) 
        #create a session
        request.session['logged_user'] = new_user.id
        return redirect("/user/dashboard")
    return redirect('/')    

#Login user_________________________________
def login_user(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        this_user = User.objects.filter(email=request.POST['email'])
        if this_user:
            log_user = this_user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()): 
                request.session['logged_user'] = log_user.id  
                return redirect('/user/dashboard')
            messages.error(request, "email or password are incorrect.")
    return redirect('/')

#Dashboard_________________________________
def dashboard(request):
    if 'logged_user' not in request.session:
        return redirect('/')
    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        #show all books
        'all_books': Book.objects.all()
    }
    return render(request, 'dashboard.html', context)
#Add book___________________________________
def add_books(request):
    if request.method == "POST":
        #validation before adding the book to DB
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/user/dashboard') 
        else:
            user = User.objects.get(id=request.session['logged_user'])
            new_book = Book.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            uploaded_by = user
            )
            #user that uploded the book, automatically likes the book
            user.user_who_liked.add(new_book)

            return redirect('/user/dashboard')
    
#Book info page______________________________
def book_info(request, book_id):
    context = {
        'the_book': Book.objects.get(id=book_id),
        'logged_user': User.objects.get(id=request.session['logged_user'])
    }
    return render(request, 'book_info.html', context)

#Add/Remove from favorites___________________
def book_add_to_fav(request, book_id):
    logged_user = User.objects.get(id=request.session['logged_user'])
    the_book = Book.objects.get(id=book_id)
    logged_user.user_who_liked.add(the_book) #getting an error!!!!

    return redirect(f'/books/book_info/{book_id}')

def book_drop_from_fav(request, book_id):
    logged_user = User.objects.get(id=request.session['logged_user'])
    the_book = Book.objects.get(id=book_id)
    logged_user.user_who_liked.remove(the_book) 

    return redirect(f'/books/book_info/{book_id}')

#Update description__________________
def update_book(request, book_id):
    the_book = Book.objects.get(id=book_id)
    the_book.description = request.POST['description']
    the_book.save()
    return redirect(f'/books/book_info/{book_id}')

#Delete book____________________
def delete_book(request, book_id):
    the_book = Book.objects.get(id=book_id)
    the_book.delete()
    return redirect('/user/dashboard')

#Logout user_________________________________
def logout_user(request):
    request.session.flush()
    return redirect('/')