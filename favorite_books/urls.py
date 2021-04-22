from django.urls import path, include

urlpatterns = [
    path('', include('fav_books_app.urls')),
]
