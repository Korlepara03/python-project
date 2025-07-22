from django.urls import path
from AdminApp import views
urlpatterns = [
    path('', views.index),
    path('loginaction', views.loginaction),
    path('AdminHome', views.AdminHome),
    path('UploadDataset', views.UploadDataset),
    path('Preprocess', views.Preprocess),
    path('BuildKNN', views.BuildKNN),
    path('RecommendBook',views.RecommendBook),
    path('RecommendAction', views.RecommendAction),
    path('userlogin', views.userlogin),
    path('uloginaction', views.uloginaction),
    path('regaction', views.regaction),
    path('register', views.register),
    path('UserHome', views.UserHome),
]
