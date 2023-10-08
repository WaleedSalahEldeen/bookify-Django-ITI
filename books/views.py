from django.shortcuts import render,HttpResponse,redirect
from books.forms import BookForm
from books.models import Book
# Create your views here.


def index(request):
    # return HttpResponse("Hello World")
    books = Book.objects.all()
    return render(request, 'books/index.html', {'books': books})



def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

def edit_book(request, book_id):
    book = Book.get_book(id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form})

def delete_book(request, book_id):
    book = Book.get_book( id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('dashboard')
    return render(request, 'books/delete_book_confirm.html', {'book': book})

def book_detail(request, book_id):
    book = Book.get_book( id=book_id)
    context = {
        'book': book,
    }
    return render(request, 'books/book_detail.html', context)

