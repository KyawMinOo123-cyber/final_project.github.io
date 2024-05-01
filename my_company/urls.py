from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('current_services',views.current_services,name='current_services'),
    path('create_service',views.create_service,name='create_service'),
    path('about',views.about,name="about"),

    path('all_services/<int:service_id>',views.delete_service,name="delete_service"),
    path('admin',admin.site.urls, name = 'admin'),

    path('user_status',views.user_status,name="user_status"), ##still not used
    path('all_services',views.all_services,name="all_services"),

    path('employees',views.employees,name="employees"),
    path('career',views.career,name = 'career'),
    path('create_career',views.create_career,name = 'create_career'),
    path('career_info/<int:career_id>',views.career_info,name = 'career_info'),
    path('edit_career/<int:career_id>',views.edit_career,name = 'edit_career'),
    path('update_description/<int:description_id>',views.update_description,name = "update_description"),
    path('all_careers',views.all_careers,name = "all_careers"),
    path('all_careers/<int:career_id>',views.delete_career,name = "delete_career"),
    path('apply_job/<int:career_id>',views.apply_job,name="apply_job"),
    path('job_application/<int:career_id>',views.job_application, name = 'job_application'),

    #all job applications for admin
    path('job_applications',views.job_applications,name = 'job_applications')
]