from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . models import *
from .forms import ServiceForm,CareerForm,JobApplicationForm
from django.utils import timezone
import json
# Create your views here.



def index(request):
    user = request.user
    notifications = Notification.objects.filter(user = user, is_read = False)

    return render(request,'my_company/index.html',{
        "notification":notifications
    })

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
    services = Service.objects.order_by('-timestamp').all()
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


def career(request):
    careers = Career.objects.order_by('-timestamp').all()
    return render(request,'my_company/career.html',{
        "careers":careers
    })

def career_info(request,career_id):
    career = Career.objects.get(pk = career_id)
    return JsonResponse( career.serialize() , safe = False)

def all_careers(request):
    careers = Career.objects.all()
    return JsonResponse([career.serialize() for career in careers],safe = False)


def delete_career(request,career_id):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            career = Career.objects.get(pk = career_id)
            career.delete()
        else:
             return render(request,'my_company/career.html',{
            "error":"Permission Denied!!"
        })
        
    else:
        return render(request,'my_company/career.html',{
            "error":"Permission Denied!!"
        })


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



def create_career(request):
    user = request.user
    if user.is_staff:
        if request.method == "POST":
            form = CareerForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('career'))
        else:
            form = CareerForm()
            
        return render(request,'my_company/career.html',{
                "form":form
        })
    else:
        return render(request,'my_company/career.html',{
            "error": "Permission denied!"
        })


def employees(request):
    user = request.user
    if user.is_staff:
        employees = Employee.objects.all()
        return render(request, 'my_company/employees.html',{
            "employees":employees
        })
    else:
        return JsonResponse({"error":"Only Staff Members Can View This Page!"})

def edit_career(request,career_id):
    user = request.user
    if user.is_staff:
        career = Career.objects.get(pk= career_id)
        return render(request,'my_company/editForm.html',{
            "career":career
        })

def update_description(request,description_id):
    user = request.user
    try:
        career = Career.objects.get(pk = description_id)
    except Career.DoesNotExist:
        return JsonResponse({'error':"Career Does Not Exist"},status = 404)
    
    if user.is_staff:
        if request.method == "POST":
            json_data = json.loads(request.body)
            description = json_data.get('description')

        Career.objects.filter(pk = description_id).update(job_description = description,timestamp = timezone.now())
        return JsonResponse({'updated_career':career.serialize()})

    else:
        return JsonResponse({"error":"Permission denied"},status = 403)


def apply_job(request,career_id):
    user = request.user
    if not Career.objects.filter(id = career_id).exists():
         return render(request,'my_company/career.html',{
            "error":"Career does not exists!"
        })
    else: 
        if user.is_staff:
            return render(request,'my_company/career.html',{
                "error":"This user cannot apply for the position!"
            })
        else:
            career = Career.objects.get(pk = career_id)
            return render(request,"my_company/apply_job_form.html",{
                "career":career
            })


def job_application(request,career_id):
    career = Career.objects.get(pk = career_id)
    user = request.user
    if not Career.objects.filter(id = career_id).exists():
        return render(request,'my_company/career.html',{
            "error":"Career does not exists!"
        })
    else:
        if user.is_staff:
            return render(request,'my_company/career.html',{
                "error":"This user cannot applied for the position!"
            })

        else:
            if user.is_authenticated:
                if request.method == "POST":
                    job_applier = request.POST.get('job_applier')
                    position = request.POST.get('position')
                    expected_salary = request.POST.get('expected_salary')
                    contact_number = request.POST.get('contact_number')
                    cover_letter = request.POST.get('cover_letter')
                    apply_date = request.POST.get('apply_date')

                    job_application = Job_application_form(
                        applying_user=request.user,
                        job_applier=job_applier,
                        position=position,
                        expected_salary=expected_salary,
                        contact_number=contact_number,
                        cover_letter=cover_letter,
                        apply_date=apply_date
                    )
                    career.applied_users.add(request.user)
                    job_application.save()
                   
                else:
                    return render(request,'my_company/career.html',{
                        "error":"The form you're trying to submit is invalid!"
                    })
            else:
                return JsonResponse({"error":"You need to login first!"},status = 302)
    
    return HttpResponseRedirect(reverse('career'))


#Job applications for Admin

def add_to_interview(request,application_id):
    application = Job_application_form.objects.get(pk = application_id)    
    if request.user.is_staff:
        application.interview = True
        application.save()
        return JsonResponse({"success": "Form successfully added to interviewing list!"})
    else:
        return JsonResponse({"error": "Only staff members are allowed to perform this action."})

def job_applications(request):
    new_applications = Job_application_form.objects.filter(interview = False)

    if Job_application_form.objects.filter(interview = True).exists():
        interviewing_applications = Job_application_form.objects.filter(interview = True)
        return render(request,'my_company/all_applications.html',{
            "new_applications" : new_applications,
            "interviewing_applications": interviewing_applications
        })
    else:
        return render(request,'my_company/all_applications.html',{
            "new_applications" : new_applications
        })


def new_application_info(request,application_id):
    application = Job_application_form.objects.get(pk =  application_id)
    return JsonResponse(application.serialize(), safe = False)

def reject_application(request,application_id):
    user = request.user
    rejectApplication = Job_application_form.objects.get(pk = application_id) 
    if user.is_staff:
        rejectApplication.delete()
        return JsonResponse({"success":"Application deleted successfully"},status = 200)
    else:
        return JsonResponse({"error":"Permission Denied"}, status = 403)


def employee_hiring_form(request,application_id):
    user = request.user
    if user.is_staff:
        application = Job_application_form.objects.get(pk = application_id)
        return JsonResponse(application.serialize(), safe=False)
    else:
        return JsonResponse({"error":"Only staff members can perform this action!"} , status = 403)
    

def save_employee_info(request,application_id):
    user = request.user
    if user.is_staff:
        application = Job_application_form.objects.get(pk = application_id)

        if request.method == "POST":
            data = json.loads(request.body)

            try:
                applier_id = data.get("applier_id")
                name = data.get("name")
                positions = data.get('positions')
                team = data.get('team')
                gender = data.get("gender")
                department = data.get("department")
                salary = data.get("salary")
                address = data.get("address")
                contact_number = data.get('contact_number')
                hiring_date = data.get('hiring_date')

                all_teams = Team.objects.all()
                team_names = [team_obj.name.lower() for team_obj in all_teams]

                if team.lower() not in team_names:
                    return JsonResponse({'error': "Please provide a team that's already existing!"}, status=400)
                else:
                    applier = User.objects.get(pk = applier_id)
                    employee = Employee(
                        applier = applier,
                        name = name,
                        positions = positions,
                        team = team,
                        gender = gender,
                        department = department,
                        salary = salary,
                        address = address,
                        contact_number = contact_number,
                        hiring_date = hiring_date if hiring_date else timezone.now(),
                        hired = True
                    )

                    employee.save()
                    application.delete()
                    return JsonResponse({
                    'status': 'success',
                    'message': 'Employee data received and employee created successfully'
                    })

            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

        else:
            return JsonResponse({"error":'Method not allowed'}, status=405)
    else:
        return JsonResponse({"error":"Only staff members can perform this action!"}, status=403)


def create_team(request):
    user = request.user
    if user.is_staff:
        if request.method == "POST":
            name = request.POST.get('name')
            if name and len(name) <= 10:
                team = Team(name = name)
                team.save()
            else:
                return JsonResponse({"error":"Invalid data"}, status=400)
        return HttpResponseRedirect('/employees')
    else:
        return JsonResponse({'error':"Only staff members can perform this action!"},status = 403)
    

def team_list(request):
    user = request.user
    if user.is_staff:
        teams = Team.objects.all()
        serialized_teams = [team.serialize() for team in teams]
        return JsonResponse(serialized_teams,safe = False)
    else:
        return JsonResponse({"error":"Only staff members can perform this action!"}, status = 403)


def delete_team(request,team_id):
    user = request.user
    if user.is_staff:
        if request.method == "POST":
            data = json.loads(request.body)
            teamID = data.get("id")

            team_to_delete = Team.objects.get(pk = teamID)
            team_to_delete.delete()
            return JsonResponse({"Success":"Team deleted successfully!"})
        else:
            return JsonResponse({"error":'Method not allowed'}, status=405)
    else:
        return JsonResponse({"ERROR":"Only staff members can perform this action!"},status= 403)


def edit_employee(request,employee_id):
    user = request.user
    if user.is_staff:
        employee = Employee.objects.get(pk = employee_id)
        return JsonResponse(employee.serialize(), safe = False)
    else:
        return JsonResponse({"error":"Only staff members can perform this action!"}, status = 403)


def fire_employee(request,employee_id):
    user = request.user
    if user.is_staff:
        employee = Employee.objects.get(pk = employee_id)
        employee_user = User.objects.get(pk = employee.applier.id)
        notification_message = "You Have Been Fired From Your Position!"
        Notification.objects.create(user = employee_user,message = notification_message)

        employee.delete()

        return JsonResponse({"success":"Employee Fired Successfully!"})
    else:
        return JsonResponse({"error":"Only staff members can perform this action!"},status = 403)


def update_employee(request,employee_id):
    user = request.user
    if user.is_staff:
        employee = Employee.objects.get(pk = employee_id)
        if request.method == "POST":
            data = json.loads(request.body)

            new_position = data.get('position')
            new_team = data.get('team')
            new_department = data.get('department')
            new_salary = data.get('salary')
            new_address = data.get('address')
            new_number = data.get('contact_number')

            all_teams = Team.objects.all()
            team_names = [team_obj.name.lower() for team_obj in all_teams]

            if new_team.lower() not in team_names:
                return JsonResponse({'error': "Please provide a team that's already existing!"}, status=400)
            else:
                employee.positions = new_position
                employee.team = new_team
                employee.department = new_department
                employee.salary = new_salary
                employee.address = new_address
                employee.contact_number = new_number

                employee.save()
                return JsonResponse({"success":"Employee Details Updated Successfully!"})
        else:
            return JsonResponse({"error":"Method Not Allowed!"}, status = 405)
    else:
        return JsonResponse({"error":"Only staff members can perform this action"}, status = 403)



