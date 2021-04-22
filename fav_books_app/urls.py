from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('user/register', views.register_user),
    path('user/login', views.login_user),
    path('user/dashboard', views.dashboard),
    path('books/add', views.add_books),
    path('user/logout', views.logout_user),
    path('books/book_info/<int:book_id>', views.book_info),
    path('books/<int:book_id>/add_to_fav', views.book_add_to_fav),
    path('books/<int:book_id>/drop_from_fav', views.book_drop_from_fav),
    path('books/<int:book_id>/update', views.update_book),
    path('books/<int:book_id>/delete', views.delete_book),
]
