from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . models import *
from .forms import ServiceForm
# Create your views here.


def index(request):
    return render(request,'my_company/index.html')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "my_company/register.html", {
                "error": "Passwords did not matched!"
            })
        else:    
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "my_company/register.html", {
                    "error": "Username already taken."
                })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "my_company/register.html") 



def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "my_company/login.html", {
                "error": "Invalid username or password."
            })
    else:
        return render(request, "my_company/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def all_services(request):
    all_service = Service.objects.all()
    services = all_service.order_by("-timestamp").all()
    return JsonResponse([service.serialize() for service in services],safe=False)


def user_status(request):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            return JsonResponse({"is_staff":True},safe=False)
        else:
            return JsonResponse({"is_staff":False},safe=False)
    else:
        return JsonResponse({"login":False},safe=False)


def current_services(request):
    services = Service.objects.all()
    return render(request,'my_company/current_services.html',{
        'services':services
    })

def about(request):
    return render(request,'my_company/about.html')

def delete_service(request,service_id):
    user = request.user

    if user.is_authenticated:
        if user.is_staff:
            if request.method == "POST":
                service = Service.objects.get(pk = service_id)
                service.delete()

            if request.method == "GET":
                service = Service.objects.get(pk = service_id)
                return JsonResponse(service.serialize(),safe=False)
    
    if request.method == "GET":
        service = Service.objects.get(pk = service_id)
        return JsonResponse(service.serialize(),safe=False)


@login_required


def create_service(request):
    user = request.user
    if user.is_staff:
        if request.method == 'POST':
            form = ServiceForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('current_services'))
        else:
            form = ServiceForm()
            return render(request,'my_company/current_services.html',{
                "form":form
            })
    else:
        return render(request,'my_company/current_services.html',{
            "error": "Permission denied!"
        })







def employees(request):
    return render(request, 'my_company/employees.html')