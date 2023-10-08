from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='books/covers/', null=True, blank=True)
    availability_status = models.BooleanField(default=True, )
    borrowed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    borrow_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    @classmethod
    def get_all_books(cls):
        return cls.objects.all()

    @classmethod
    def get_book(cls, id):
        return cls.objects.get(id=id)

    @classmethod
    def delete_book(cls, id):
        return cls.objects.get(id=id).delete()

    def is_available(self):
        return self.borrowed_by is None

    def borrow(self, student):
        if self.is_available():
            self.borrowed_by = student
            self.borrow_date = datetime.now()
            self.return_date = datetime.now() + timedelta(days=7) 
            self.availability_status = False
            self.save()
            return True
        return False

    def return_book(self):
        self.borrowed_by = None
        self.borrow_date = None
        self.return_date = None
        self.availability_status = True
        self.save()
