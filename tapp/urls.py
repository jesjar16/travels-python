#from dojo import views_ajax
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="my_index"),
    path('success/', views.success, name="my_success"),
    path('register/', views.register, name="my_register"),
    path('login/', views.login, name="my_login"),
    path('homepage/', views.homepage, name="my_homepage"),
    path('travels/', views.travels, name="my_travels"),
    path('add/', views.add, name="my_add"),
    path('create/', views.create, name="my_create"),
    path('join/<int:trip_id>/', views.join, name="my_join"),
    path('destination/<int:trip_id>/', views.destination, name="my_destination"),
    path('about/', views.about, name="my_about"),
    path('logout/', views.logout, name="my_logout"),
]