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

    path('employees',views.employees,name="employees")
]