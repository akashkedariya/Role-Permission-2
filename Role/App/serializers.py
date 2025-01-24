from rest_framework import serializers
from .models import CustomUser, Employee



class CustomuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    # def create(self, validated_data):
    #     password  = validated_data.pop('password')

    #     user = super().create(validated_data)
    #     user.set_password(password)
    #     user.save()

    #     return user

    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = CustomUser(email = validated_data['email'])
        print('=====11111')
        user.set_password(password)
        user.save()

        return user


class CustomUserloginSerializers(serializers.ModelSerializer) :
    email=serializers.EmailField(max_length=255)
    class Meta :

        model = CustomUser
        fields = [ 'email', 'password' ]        


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta :
        model = Employee
        fields = '__all__'
