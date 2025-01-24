from django.shortcuts import render
from .models import CustomUser, Employee
from .serializers import CustomuserSerializer, CustomUserloginSerializers, EmployeeSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics     
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import filters



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class Loginuser(APIView) :

    def post(self,request,format=None):

        email = request.data.get('email')
        password = request.data.get('password')
        print('email : ',email)
        user = authenticate(email=email,password=password)
        print('====user==',user)
        
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg':'login success','token':token},status=status.HTTP_200_OK)
        
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid please enter currect credential. ']}},status=status.HTTP_200_OK)  


class Customuserview(APIView):
    def post(self, request) :
        serializer = CustomuserSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            print('=====22222')

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def custom_authentication_required(view_func):
    def wrapper(request, *args, **kwargs):
        print('====user===',request.user)
        if not CustomUser.objects.filter(email = request.user,role = 'manager').exists():  # try role wise user

            return Response(
                {'detail': 'User not valid'},
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request)
    
    return wrapper 

from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk=None):

    if request.method == 'GET':
        token = request.headers.get("Authorization")
        # print('==token===',token)
        if token :
            token = token.replace("Bearer ", "")
            print('===token====',token)
            user, _ = JWTAuthentication().authenticate(request)
            print('===user==',user.password,type(user.role))
            print('===---==',_)

            if user.role != 'developer':
                return Response({'msg' : 'Not valid user'})

            result = CustomUser.objects.all()  
            
            data = [{'first_name': i.first_name, 'role':i.role, 'email' : i.email } for i in result]

            print('===This is a new person ===',data)
            
            data  = {
                'msg' : data
            }

        else:
            
               data = {
                   'msg' : 'Not access'
                    } 
            
        return Response(data)


#======OR===============================================

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# @custom_authentication_required
# def snippet_detail(request, pk=None):

#     if request.method == 'GET':
#         data  = {
#             'msg' : 'Success'
#         }
#         return Response(data)




class CustomUserView_permission(APIView):
    permission_classes = [IsAuthenticated]

    # @method_decorator(custom_authentication_required)
    def get(self, request):
        # print('====Working====')
        
        return Response({'data' : "Get data successfully"}, status=status.HTTP_200_OK)

        
class UserList(generics.ListAPIView):
    # def get(self,request):
    print('==Working====')
    queryset = CustomUser.objects.all()
    serializer_class = CustomuserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['role','first_name']
    # ordering_fields = ['first_name']

    # filterset_fields = ['role']

    # print('===filter===',filterset_fields)
        

class EmployeeList(generics.ListAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['age']

    # search_fields = ['emp_name__user__role']
    
    # ordering_fields = ['city']        


# class ProjectListView(generics.ListAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['name']
#     # search_fields = ['name', 'description','project_manager__user__f_name']      # 'project_manager__-->user__-->f_name' (ForeignKey)
#     filterset_fields = ['description','name']                                           # Whole description   
#     ordering_fields = ['name']        