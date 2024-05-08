"""
URL configuration for bookmyshow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/organizer', AddOrganizer.as_view()),
    path('city/', GetAddCity.as_view()),
    path('delete-city/<int:pk>', DeleteCity.as_view()),
    path('language', GetAddLanguages.as_view()),
    path('movie', GetAddUpdateMovies.as_view()),
    path('casts', GetAddDeleteUpdateCasts.as_view()),
    path('movie/theater', GetAddMovieTheater.as_view()),
    path('movie/screen', AddGetMovieScreen.as_view()),
    path('movie/seat', AddGetMovieSeat.as_view()),
    path('movie/show', AddMovieShow.as_view()),
    path('movie/show/screen', AddMovieShowScreen.as_view()),
    path('search/movies', SearchMoviesByCity.as_view()),
    path('search/movie/screen', MovieScreeningDetails.as_view()),
    path('search/movie/screen/seats', GetMovieShowSeats.as_view()),
    path('book/movie', CreateBooking.as_view()),
    path('payment/confirm', MakePayment.as_view()),
    path('ticket/verify', VerifyTicket.as_view()),
]
