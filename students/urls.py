from django.urls import path
from students import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/admin', views.admin_dashboard, name='dashboard'),
    path('dashboard/student', views.student_dashboard, name='student_dashboard'),
    path('dashboard/student/update', views.update_profile, name='update_profile'),
    path('dashboard/student/<int:student_id>/', views.view_student, name='view_student'),
    path('dashboard/change_password', views.change_password, name='change_password'),
    path('dashboard/search/', views.search, name='search'),
    path('book/borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('book/return/<int:book_id>/', views.return_book, name='return_book'),
]