"""
URL configuration for quiz_daily project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('change-language/<str:lang>/', views.change_language, name='change_language'),
    path('quiz/cro/', views.quiz, {'lang': 'cro'}, name='quiz-cro'),
    path('quiz/eng/', views.quiz, {'lang': 'eng'}, name='quiz-eng'),
    path('quiz/ger/', views.quiz, {'lang': 'ger'}, name='quiz-ger'),
    path('accounts/register', views.RegisterView, name='register'),
    path("accounts/", include("django.contrib.auth.urls")),

]


