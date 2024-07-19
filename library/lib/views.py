from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import *
from django . shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



# def loginn(request):
#     if request.user.is_authenticated:
#         return redirect('/')
#     if request.method=="POST":
#         username = request.POST.get('username').lower()
#         password = request.POST.get('password')
#         try:
#             user = User.objects.get(username=username)
#         except:
#             messages.error(request,"user does not exist")
#         user = authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             return redirect('/')
#         else:
#             messages.error(request,"invalid credentials")
    

#     return render(request, 'login.html')


def loginn(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the provided email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print("User does not exist")
            messages.error(request, "Invalid credentials. Please check your email and password.")
            return render(request, 'login.html')

        # Authenticate the user using email and password
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            # Login the user
            login(request, user)
            return redirect('/')
        else:
            print("Invalid credentials")
            messages.error(request, "Invalid credentials. Please check your email and password.")
            return render(request, 'login.html')

    return render(request, 'login.html')



    


def signup(request):
    try:
        if request.method == 'POST':
            username = request.POST.get("firstname")
            email = request.POST.get("email")
            usn = request.POST.get("usn")
            password = request.POST.get("password")
            first_name = request.POST.get("firstname")
            last_name = request.POST.get("lastname")

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                messages.error(
                    request, 'Email is already registered. Use a different email.')
                return redirect('signup')

            my_user = User.objects.create_user(username, email, password)

            # Create the Student object and associate it with the User
            user = Student.objects.create(
                user=my_user,
                student_id=usn,
                email=email,
                first_name=first_name,
                last_name=last_name,

            )

            my_user.save()
            user.save()

            user = authenticate(request, username=username, password=password)
            login(request, user)

            return redirect('home')

    except Exception as e:
        print(f"Error during signup: {e}")
        messages.error(request, 'An error occurred during signup.')
        return redirect('signup')

    return render(request, 'signup.html')


@login_required(login_url='login/')
def home(request):
    recently_added_books = Book.objects.order_by('-id')[:3]
    all_books = Book.objects.all()
    book_list = list(all_books)
    all_genres = Genre.objects.all()
    context = {
        'recently_added_books': recently_added_books,
        'all_books': all_books,
        'all_genres': all_genres,
        'book_list': book_list,
    }
    return render(request, 'home.html', context)


@login_required(login_url='login/')
def logoutt(request):
    print("logging out ", request.user)
    logout(request)
    return redirect('/')


@login_required(login_url="login/")
def borrow(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        student = Student.objects.get(email=request.user.email)

        # Check if the student already has 2 books
        if student.book1 and student.book2:
            messages.error(
                request, 'You can only borrow a maximum of 2 books.')
            return redirect('borrow')

        try:
            # Try to find the book by ISBN number
            book = Book.objects.get(isbn_number=isbn, is_available=True)
        except Book.DoesNotExist:
            messages.error(request, 'Book not found or already borrowed.')
            return redirect('borrow')

        # Update student's book1 or book2 and mark the book as unavailable
        if not student.book1:
            student.book1 = book
        elif not student.book2:
            student.book2 = book

        book.is_available = False

        student.save()
        book.save()
        messages.success(
            request, f'Book "{book.title}" borrowed successfully!')
        return redirect('sucess')

    return render(request, 'borrow.html')


@login_required(login_url='login/')
def sucess(req):
    return render(req, 'sucess.html')


@login_required(login_url='login/')
def return_book(request):
    if request.method == 'POST':
        isbn_num = request.POST.get('isbn')
        print(f"isbn_num is {isbn_num}")
        try:
            book = Book.objects.get(isbn_number=isbn_num)
            
            student = Student.objects.get(email=request.user.email)

            # Check if the book is assigned to the student
            if student.book1 == book or student.book2 == book:
                # Update the book availability and remove from student's book list
                book.is_available = True
                book.save()

                if student.book1 == book:
                    student.book1 = None
                elif student.book2 == book:
                    student.book2 = None

                student.save()

                messages.success(
                    request, f'Book with ISBN {isbn_num} returned successfully.')
            else:
                messages.error(request, 'You have not borrowed this book.')
        except Book.DoesNotExist:
            messages.error(
                request, 'Book with the provided ISBN does not exist.')

    return render(request, 'return_book.html')


@login_required(login_url='login/')
def profile(request):
    user_profile = Student.objects.get(email=request.user.email)

    context = {'user_profile': user_profile}

    if user_profile.book1:
        context['book1'] = Book.objects.get(book_id=user_profile.book1.book_id)

    if user_profile.book2:
        context['book2'] = Book.objects.get(book_id=user_profile.book2.book_id)

    return render(request, 'profile.html', context)
