from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='list'),
    path('<int:pk>/', views.book_detail, name='detail'),
    path('api/', views.book_api_list, name='api_list'),
    path('api/<int:pk>/', views.book_api_detail, name='api_detail'),
]