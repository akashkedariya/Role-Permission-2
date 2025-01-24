from django.urls import path
from . import views

urlpatterns = [
    
    path('user-register/',views.Customuserview.as_view()),
    path('user-login/',views.Loginuser.as_view()),
    path('view-access/',views.CustomUserView_permission.as_view()),
    path('demo/',views.snippet_detail),
    path('search/',views.UserList.as_view()),
    path('emp_search/',views.EmployeeList.as_view()),

]