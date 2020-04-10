from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt
from datetime import datetime

def index(request):
    return render(request, "index.html")

def createUser(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            print("User's password entered was " + request.POST['password'])
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],date_of_birth=request.POST['dob'], password=hashed_pw)
            print("User's password has been changed to " + user.password)
            print("User's First Name:" + user.first_name)
            print("User's Last Name:" + user.last_name)
            print("User's Email:" + user.email)
            print("Date of Birth: " + user.date_of_birth)
    return redirect('/')

def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]                    
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id #IMPORTANT!!!
                return redirect('/home')
            else:
                print("Password didn't match")
                messages.error(request, "Incorrect name or password")
        else:
            print("Name not found")
            messages.error(request, "Incorrect name or password")
    return redirect('/')

def home(request):
    if request.method == "GET":
        if "user_id" in request.session:
            context = {
                "user": User.objects.get(id=request.session['user_id']),
                "allbooks": Book.objects.all(),
                "age": int((datetime.now().date() - (datetime.strptime(str(User.objects.get(id=request.session['user_id']).date_of_birth), "%Y-%m-%d").date())).days / 365),
            }
            return render(request, "home.html", context)
        else:
            return redirect('/')

def addBook(request):
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            Book.objects.create(title = request.POST['title'], desc = request.POST['desc'], uploaded_by = User.objects.get(id = request.session['user_id']))
            bookadded = Book.objects.get(title= request.POST['title'])
            bookadded.users_who_liked.add(User.objects.get(id=request.session['user_id']))
    return redirect('/home')

def book(request, id):
    if "user_id" in request.session:
        context = {
            "allbook": Book.objects.get(id=id),
            "user": User.objects.get(id=request.session['user_id']),
            "age": int((datetime.now().date() - (datetime.strptime(str(User.objects.get(id=request.session['user_id']).date_of_birth), "%Y-%m-%d").date())).days / 365),
        }
        return render(request, "book.html", context)

def AddFav(request, id):
    if request.method == "POST":
        BookFav = Book.objects.filter(id=id)
        if BookFav:
                book = BookFav[0]
                book.users_who_liked.add( User.objects.get(id=request.session['user_id']))
        return redirect('/home')

def AddFavBook(request, id):
    if request.method == "POST":
        BookFav = Book.objects.filter(id=id)
        if BookFav:
                book = BookFav[0]
                book.users_who_liked.add( User.objects.get(id=request.session['user_id']))
        return redirect('/book/'+str(id))

def RemoveFav(request, id):
    if request.method == "POST":
        BookUnFav = Book.objects.filter(id=id)
        if BookUnFav:
                book = BookUnFav[0]
                book.users_who_liked.remove( User.objects.get(id=request.session['user_id']))
    return redirect('/home')

def RemoveFavBook(request, id):
    if request.method == "POST":
        BookUnFav = Book.objects.filter(id=id)
        if BookUnFav:
                book = BookUnFav[0]
                book.users_who_liked.remove( User.objects.get(id=request.session['user_id']))
    return redirect('/book/'+str(id))

def edit(request, id):
    update = Book.objects.get(id=id)
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/book/'+str(id)) #Go back to the place of the form
    else:
        if request.method == "POST":
            update.title = request.POST['title']
            update.desc = request.POST['desc']
            update.save()
        return redirect('/book/'+ str(id))

def erase(request, id):
    if request.method == "POST":
        bookToDelete = Book.objects.filter(id=id)
        if bookToDelete:
                book = bookToDelete[0]
                user = User.objects.get(id=request.session['user_id'])
                if book.uploaded_by == user:
                    book.delete()
    return redirect('/home')

def logout(request):
    if request.method == "POST":
        request.session.clear()
    return redirect('/')