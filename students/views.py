# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from books.models import Book
from django.contrib.auth.models import User
from students.forms import ProfileUpdateForm, PasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST': 
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('dashboard')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})




@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('student_dashboard')

    all_books = Book.objects.all()
    borrowed_books = Book.objects.exclude(borrowed_by=None)
    all_users = User.objects.all()
    
    context = {
        'all_books': all_books,
        'borrowed_books': borrowed_books,
        'all_users': all_users
    }
    return render(request, 'dashboard/admin.html', context)

@login_required
def student_dashboard(request):
    student_books = Book.objects.filter(borrowed_by=request.user)
    context = {
        'student_books': student_books,
    }
    return render(request, 'dashboard/student.html', context)

@login_required
def update_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'dashboard/update_profile.html', {'form': form})

def view_student(request, student_id):
    student = User.objects.filter(id=student_id)[0]
    # print(student)
    return render(request, 'dashboard/view_student.html', {'student': student})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password1"]
            confirm_password = form.cleaned_data["new_password2"]

            if request.user.check_password(old_password):
                if new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    return redirect('dashboard')
                else:
                     return redirect('dashboard')
            else:
                 return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/change_password.html', {'form': form})

@login_required
def borrow_book(request, book_id):
    book = Book.get_book(id=book_id)
    
    if book.is_available() and request.method == "POST":
        book.borrow(request.user)
        return redirect('index')
    else:
        return redirect('book_detail', book_id=book.id) 

@login_required
def return_book(request, book_id):
    book = Book.get_book(id=book_id)
    book.return_book()
    return redirect('book_detail', book_id=book.id) 

def user_logout(request):
    logout(request)
    return redirect('index')  

def search(request):
    if request.method == "POST":
        search_id = request.POST['search']
        student = User.objects.filter(id=search_id)[0]
        return render(request, 'dashboard/view_student.html', {'student': student})
    return redirect('dashboard') 
