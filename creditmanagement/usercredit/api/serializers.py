from rest_framework import serializers
from usercredit.models import *
from core.emails import *
from django.core.validators import MaxValueValidator, MinValueValidator
percentage_validators=[MinValueValidator(0.1), MaxValueValidator(100)]
from core.response import *

#------------------- USER REGISTRATION SERIALIZER -----------------------#

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    # tc = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['id','profile_pic','first_name', 'last_name','password', 'password2','email', 'phone_no', 'aadhar', 'pan', 'cheque', 'refer_code', 'referred_by', 'under_by', 'tc', 'created_by', 'modified_by', 'user_created_at', 'user_modified_at']

        extra_kwargs = {
            'password' : {'write_only' : True},
        }

    # def validate(self, attrs):
    #     password = attrs.get('password')
    #     password2 = attrs.get('password2')
    #     tc = attrs.get('tc')

    #     if tc == False:
    #         raise serializers.ValidationError("Terms and Condition (tc) must be true !")

    #     if password != password2:
    #         return badRequest("Password and Confirm password doesn't matched !!!")

        # return super().validate(attrs)

    def create(self, validated_data):
        validated_data["refer_code"] = generate_ref_code()
        validated_data["role"] = 2
        
        return User.objects.create_user(**validated_data)


#------------------ ADMIN REGISTRATION SERIALIZER  --------------------------#

class AdminRegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ["id",'profile_pic','first_name', 'last_name','password','password2','email', 'phone_no']

        extra_kwargs = {
            'password' : {'write_only' : True},
        }

    def create(self, validated_data):
        validated_data["role"] = 1
        validated_data["refer_code"] = generate_ref_code()
        return User.objects.create_admin(**validated_data)


#--------------------- LOGIN SERIALIZER (ADMIN, USER) -------------------#

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']


#------------------- RESEND OTP SERIALIZER (ADMIN, USER) ---------------#

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

#------------------ VERIFY ACCOUNT (ADMIN, USER) -----------------------#

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp  = serializers.CharField()


#---------------- VERIFY RESET PASSWORD OTP (ADMIN, USER) ---------------#

class VerifyPasswoprdOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp  = serializers.CharField()


#------------------ USERS LIST (ADMIN ACCESS) ----------------------------#

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name','email', 'phone_no', 'aadhar', 'pan', 'cheque', 'tc', 'is_verified', 'is_active', 'otp_verified' ]
        # exclude = ['password', 'groups', 'user_permissions']


#-------------- USER PROFILE SERIALIZER (USER) --------------------------#
 
class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only = True)
    phone_no = serializers.CharField(read_only = True)

    class Meta:
        model = User
        fields = ['profile_pic', 'first_name', 'last_name','email', 'phone_no', 'aadhar', 'pan',  'cheque']


#-------------- EDIT USER PROFILE SERIALIZER (ADMIN ACCESS) ----------------------#
 
class editUserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only = True)
    phone_no = serializers.CharField(read_only = True)

    class Meta:
        model = User
        fields = ["id",'profile_pic', 'first_name', 'last_name','email', 'phone_no', 'aadhar', 'pan',  'cheque', 'modified_by', 'user_modified_at']



#--------------- ADMIN PROFILE SERIALIZER (ADMIN) --------------------------#

class AdminProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only = True)
    phone_no = serializers.CharField(read_only = True)

    class Meta:
        model = User
        fields = ['profile_pic','first_name', 'last_name','email', 'phone_no']


#--------------- USER CHANGE PASSWORD (ADMIN, USER) ------------------------#

class USerChangePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password','password2']

    # def validate(self, attrs):
    #     password = attrs.get('password')
    #     password2 = attrs.get('password2')
    #     user = self.context.get('user')
    #     # if password != password2:
    #     #     # return badRequest("password and confirm password dosen't match")
    #     #     raise serializers.ValidationError("password and confirm password dosen't match")
    #     user.set_password(password)
    #     user.save()
    #     return super().validate(attrs)


#------------------ RESET PASSWORD EMAIL (ADMIN, USER) ---------------------#

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()





 






    
    

    