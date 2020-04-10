from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('users', views.createUser),
    path('login', views.login),
    path('home', views.home),
    path('addbook', views.addBook),
    path('book/<int:id>', views.book),
    path('addfav/<int:id>', views.AddFav),
    path('addfavbook/<int:id>', views.AddFavBook),
    path('removefav/<int:id>', views.RemoveFav),
    path('removefavbook/<int:id>', views.RemoveFavBook),
    path('edit/<int:id>', views.edit),
    path('erase/<int:id>', views.erase),
    path('logout', views.logout),
]