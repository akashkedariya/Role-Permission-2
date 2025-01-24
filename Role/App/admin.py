from django.contrib import admin
from .models import CustomUser, Employee
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'role','email', 'password']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'emp_name', 'age', 'city']    
