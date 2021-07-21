from django.shortcuts import render, redirect
from django.urls import reverse
from tapp.models import User, Trip
from django.contrib import messages
import bcrypt
from django.db import IntegrityError
from tapp.decorators import login_required
from django.db.models import Avg # to calculate average

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    # getting form variables
    name = request.POST['name']
    username = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']
    
    # errors dict is received
    errors = User.objects.basic_validator(request.POST)
    
    # if there are errors
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        # getting the current form values
        form_data = {
            'name': name,
            'username': username
        }
        
        request.session['form_data'] = form_data
        
        return redirect(reverse("my_index"))
    else:
        # hashing password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        # creating the user
        this_user = User.objects.create(name=name, username=username, password=hashed_password) 

        # creating dictionary with user's data
        user_data = {
                'user_id': this_user.id,
                'name': this_user.name.capitalize(),
                'username': this_user.username,
                'action': 'register'
        }
        
        # saving user dictionary to session variable
        request.session['user_data'] = user_data
            
        messages.success(request, "User successfully created and logged in")
    
        return redirect(reverse("my_success"))
        
def login(request):
    # form variables are received
    username_login = request.POST['username_login']
    password_login = request.POST['password_login']
    
    # errors dict is received
    errors = User.objects.basic_validator2(request.POST)
    
    # if there are errors
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        # saving form data into form_data dictionary
        form_data = {
            'username_login': username_login
        }
        
        request.session['form_data'] = form_data
        
        return redirect(reverse("my_index"))
    else: # no errors
        user = User.objects.filter(username=username_login)
        if user:
            logged_user = user[0] 
            if bcrypt.checkpw(password_login.encode(), logged_user.password.encode()):
                # creating session variables for logged in user
                user_data = {
                    'user_id': logged_user.id,
                    'name': logged_user.name.capitalize(),
                    'username': logged_user.username,
                    'action': 'login'
                }
                
                request.session['user_data'] = user_data
                
                messages.success(request, "You have successfully login")
                
                return redirect(reverse("my_success"))
            else:
                messages.error(request, "Wrong email or password")
                
                return redirect(reverse("my_index"))
        else:
            messages.error(request, "Wrong username or password")
                
            return redirect(reverse("my_index"))

@login_required
def success(request):
    return redirect(reverse("my_travels"))
    
@login_required    
def homepage(request):
    return render(request, "homepage.html")

@login_required    
def travels(request):
    # getting current user
    id = request.session['user_data']['user_id']
    this_user = User.objects.get(id=id)
    
    # all user's trip
    all_user_trips = this_user.joiners.all().order_by('travel_date_from')
    
    # other user's trips
    other_users_trips = Trip.objects.exclude(user_who_join=this_user).order_by('travel_date_from')
    
    context = {
        'all_user_trips': all_user_trips,
        'other_users_trips': other_users_trips
    }
    
    return render(request, "travels.html", context)

@login_required    
def join(request, trip_id):
    # getting current user
    id = request.session['user_data']['user_id']
    this_user = User.objects.get(id=id)
    
    # getting trip
    this_trip = Trip.objects.get(id=trip_id)
    
    # checking if user is already joining the trip
    # getting all joiners
    joiners = this_trip.user_who_join.all()
    
    for user in joiners:
        if user == this_user:
            messages.error(request, "User is already joining this trip!")
    else: # user still not joining the trip    
        # adding user to trip
        this_user.joiners.add(this_trip)
        
        # creating success message
        messages.success(request, "You have joined this trip!")
    
    return redirect(reverse("my_travels"))

@login_required    
def destination(request, trip_id):
    # getting current trip
    this_trip = Trip.objects.get(id=trip_id)
    
    # getting user
    id = request.session['user_data']['user_id']
    this_user = User.objects.get(id=id)
    
    # getting planner
    this_planner = this_trip.planned_by
    print ("Planner", this_planner)
    
    
    # getting all joiners
    joiners = this_trip.user_who_join.all()
    
    print("Joiners, but planner ",joiners)
    
    #joiners = Trip.objects.get(id=trip_id)
    joiners_except_planner = []
    
    for user in joiners:
        if user != this_planner:
            joiners_except_planner.append(user)
            
    print ("All but planner", joiners_except_planner)
    
    context = {
        'this_trip': this_trip,
        'joiners_except_planner': joiners_except_planner
    }
    
    return render(request, "destination.html", context)
    
@login_required   
def add(request):
    return render(request, "add.html")

@login_required   
def create(request):
    print(request.POST)
    # form variables are received
    destination = request.POST['destination']
    description = request.POST['description']
    date_from = request.POST['date_from']
    date_to = request.POST['date_to']
    
    # errors dict is received
    errors = Trip.objects.basic_validator(request.POST)
       
    # if there are errors
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            
        form_data = {
            'destination': destination,
            'description': description,
            'date_from': date_from,
            'date_to': date_to
        }
        
        request.session['form_data'] = form_data
        
        return render(request, "add.html")
    else:
        # no errors
        id = request.session['user_data']['user_id']
        this_user = User.objects.get(id=id)
        
        # saves trip
        this_trip = Trip.objects.create(destination=destination, description=description, travel_date_from=date_from, travel_date_to=date_to, planned_by=this_user)
        print(this_trip)
        
        # adding user to trip
        this_user.joiners.add(this_trip)

        messages.success(request, "Trip successfully added")
        
        if 'form_data' in request.session:
            del request.session['form_data']

        #return redirect(reverse("my_book_review"))
        return redirect(reverse("my_travels"))

@login_required
def about(request):
    return render(request, "about.html")

def logout(request):
    # deleting session variables
    if 'form_data' in request.session:
        del request.session['form_data']
        
    if 'user_data' in request.session:
        del request.session['user_data']
        messages.success(request, "You have successfully logout")
    
    return redirect(reverse("my_index")) 