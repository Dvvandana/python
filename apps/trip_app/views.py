from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    if 'user_id' in request.session:
        request.session.clear()
    return render(request,'trip_app/index.html')

def register(request):
    if (request.method == 'POST'):
        errors = User.objects.basic_validator(request.POST)
        if (len(errors) > 0):
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            hashed_pwd = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
            f_name = request.POST['first_name'].strip()
            l_name = request.POST['last_name'].strip()
            cur_user = User.objects.create(first_name = f_name, last_name = l_name, email = request.POST['email'], password = hashed_pwd)
            request.session['user_id'] = cur_user.id
            return redirect("/dashboard")
    else:
        return redirect('/')

def login(request):
    if (request.method == 'POST'):
        errors = User.objects.login_validator(request.POST)
        print(len(errors))
        if (len(errors) > 0):
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            user = User.objects.filter(email = request.POST['email'])
            if len(user) > 0:
                cur_user = user[0]
                request.session['user_id'] = cur_user.id
                return redirect('/dashboard')
    else:
        return redirect('/')

def success(request):
    return render(request,'trip_app/success.html')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/')

def handle_page_not_found_404(request):
    return redirect('/')

    # url(r'^dashboard$', views.dashboard),
    # url(r'^trips/new$', views.new),
    # url(r'^trips/process_new$', views.process_new),
    # url(r'^trips/process_edit$', views.process_edit),

def dashboard(request):
    if 'user_id' in request.session:
        cur_user = User.objects.filter(id = request.session['user_id'])
        if len(cur_user) > 0:
            logged_user = cur_user[0]

            # rest_of_trips =  Trip.objects.exclude(travellers)
            # rest_of_trips = Trip.objects.exclude(travellers__in = logged_user)
            rest_of_trips = Trip.objects.exclude(id__in = User.objects.get(id = request.session['user_id'] ).trips_joined.all())
            context = {
                "logged_user" : logged_user,
                "remaining_trips" : rest_of_trips
            }
            return render(request,'trip_app/dashboard.html',context)
        else:
            return redirect('/')
    else:
        return redirect('/')
    
def new_trip(request):
    if 'user_id' in request.session:
        cur_user = User.objects.filter(id = request.session['user_id'])
        if len(cur_user) > 0:
            logged_user = cur_user[0]
            context = {
                "logged_user" : logged_user
            }
            return render(request,'trip_app/new_trip.html',context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def process_new(request):

    if request.method == 'POST':
        errors = Trip.objects.trip_validator(request.POST)
        if (len(errors) > 0):
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/trips/new')
        else:
            destination = request.POST['destination'].strip()
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            plan = request.POST['plan'].strip()
            cur_user = User.objects.get(id = request.session['user_id'])
            new_trip = Trip.objects.create(destination = destination,start_date = start_date,end_date = end_date,plan = plan,created_by = cur_user)
            new_trip.travellers.add(cur_user)
            return redirect('/dashboard')
    else:
        return redirect('/')


def process_edit(request):
    if request.method == 'POST':
        errors = Trip.objects.trip_validator(request.POST)
        if (len(errors) > 0):
            for key,value in errors.items():
                messages.error(request,value)
            return redirect(f'/trips/edit/{request.POST["trip_id"]}')
        else:
            cur_trip = Trip.objects.filter(id = request.POST['trip_id'])
            if len(cur_trip) > 0:
                editing_trip= cur_trip [0]
                
                editing_trip.destination = request.POST['destination'].strip()
                editing_trip.start_date = request.POST['start_date']
                editing_trip.end_date = request.POST['end_date']
                editing_trip.plan = request.POST['plan'].strip()
                editing_trip.save()
                return redirect('/dashboard')
            else:
                return redirect('/dashboard')
    else:
        return redirect('/')


    # url(r'^trips/edit/(?P<trip_id>)$', views.edit_trip),
    # url(r'^trips/delete/(?P<trip_id>)$', views.delete_trip),
def edit_trip(request,trip_id):
    if 'user_id' in request.session:
        cur_user = User.objects.filter(id = request.session['user_id'])
        if len(cur_user) > 0:
            logged_user = cur_user[0]
            trips = Trip.objects.filter(id = trip_id)
            if len(trips) > 0:
                context = {
                    "logged_user" : logged_user,
                    "cur_trip" : trips[0]
                }
    
                context['cur_trip'].start_date = context['cur_trip'].start_date.strftime("%Y-%m-%d")
                context['cur_trip'].end_date = context['cur_trip'].end_date.strftime("%Y-%m-%d")

                return render(request,'trip_app/edit_trip.html',context)
            else:
                return redirect('/dashboard')
        else:
            return redirect('/')
    else:
        return redirect('/')
    

# url(r'^trips/(?P<trip_id>\d+)$',views.show_trip)
def show_trip(request,trip_id):
    if 'user_id' in request.session:
        cur_user = User.objects.filter(id = request.session['user_id'])
        if len(cur_user) > 0:
            logged_user = cur_user[0]

            trips = Trip.objects.filter(id = trip_id)
            if len(trips) > 0:

                cur_trip = trips[0]
            # all_travelelrs = trip.travellers.all()
            # rest_travellers = all_travelelrs.objects.exclude(id__in = cur_trip.created_by)
            # rest_of_trips = Trip.objects.exclude(id__in = User.objects.filter(id = request.session['user_id'] ).trips_joined.all())
            # rest_of_travellers = User.objects.exclude(id__in = Trip.objects.get(id = cur_trip.id).)
            
                context = {
                    "logged_user" : logged_user,
                    "cur_trip" : cur_trip
                }
                return render(request,'trip_app/trip_details.html',context)
            else:
                return redirect('/dashboard')
        else:
            return redirect('/')
    else:
        return redirect('/')
    

# url(r'^trips/delete/(?P<trip_id>\d+)$', views.delete_trip),
def delete_trip(request,trip_id):
    if 'user_id' in request.session:
        cur_user = User.objects.filter(id = request.session['user_id'])
        if len(cur_user) > 0:
            logged_user = cur_user[0]
            trips = Trip.objects.filter(id = trip_id)
            if len(trips) > 0:
                cur_trip = trips[0]
                cur_trip.delete()
                return redirect('/dashboard')
            else:
                return redirect('/dashboard')
        else:
            return redirect('/')
    else:
        return redirect('/')

   #url(r'^trips/join/(?P<trip_id>\d+)$',views.join_trip),
def join_trip(request,trip_id):
    if 'user_id' in request.session:
        cur_user = User.objects.filter(id = request.session['user_id'])
        if len(cur_user) > 0:
            logged_user = cur_user[0]
            trips = Trip.objects.filter(id = trip_id)
            if len(trips) > 0:
                cur_trip = trips[0]
                cur_trip.travellers.add(logged_user)
                return redirect('/dashboard')
            else:
                return redirect('/dashboard')
        else:
            return redirect('/')
    else:
        return redirect('/')


#    url(r'^trips/cancel/(?P<trip_id>\d+)$',views.cancel_trip),

def cancel_trip(request,trip_id):
    if 'user_id' in request.session:
        cur_user = User.objects.filter(id = request.session['user_id'])
        if len(cur_user) > 0:
            logged_user = cur_user[0]
            trips = Trip.objects.filter(id = trip_id)
            if len(trips) > 0:
                cur_trip = trips[0]
                cur_trip.travellers.remove(logged_user)
                return redirect('/dashboard')
            else:
                return redirect('/dashboard')
        else:
            return redirect('/')
    else:
        return redirect('/')
