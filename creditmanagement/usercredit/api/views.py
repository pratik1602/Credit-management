from rest_framework.response import Response
from usercredit.models import *
from usercredit.api.serializers import *
from core.emails import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.decode import get_object
from usercredit.utils import *
from datetime import datetime
from django.contrib.auth.hashers import check_password
from email import *
from core.response import *
from django.db.models import Q
import re
# from .task import *
# from django.http import HttpResponse


#-------------- GETTING TOKENS FOR USER --------------------#

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
    

#--------------- USERS LIST (ADMIN ACCESS) ------------------#

class GetUserList(APIView):

    def get(self, request):
        token = get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin= True)
            except:
                return badRequest("No Admin found !!!")
            user_id = request.GET.get("id")
            if user_id != None or 0:
                try:
                    user_obj = User.objects.filter(under_by = get_admin, id = user_id)
                except:
                    return badRequest("No User found !!!")
            else:
                user_obj = User.objects.filter(under_by = get_admin)

            serializer = UserSerializer(user_obj, many=True)
            return onSuccess("Users List !!!",  serializer.data)         
        else:
            return unauthorisedRequest()


#------------------ VERIFY USER'S ACCOUNT (ADMIN ACCESS) ----------------#

class VerifyUserAccount(APIView):

    def post(self, request):
        token = get_object(request)
        if token:
            try:
                User.objects.get(id = token["user_id"], is_admin= True)
            except:
                return badRequest("Admin not found !!!")
            data = request.data
            if data["user_id"] != "" and data["is_verified"] != "":
                try:
                    user = User.objects.get(id = data["user_id"])
                    if data["is_verified"] == True:
                        user.is_verified = True
                        user.save()
                        return onSuccess("Account verified successfully !!!", 1)
                    else:
                        user.is_verified = False
                        user.save()
                        return onSuccess("Account unverified successfully !!!", 1)                            
                except:
                    return badRequest("User not found !!!")
            else:
                return badRequest("Fields is missing !!!")   
        else:
            return unauthorisedRequest()


#---------------- USER'S CREATE ACCOUNT (ADMIN ACCESS) -------------------#

class CreateUserAccount(APIView):
    def post(self, request):
        if not request.POST._mutable:
            request.POST._mutable = True
        token = get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin= True)
            except:
                return badRequest("Admin not found !!!")
            data = request.data 
            if data["first_name"] != "" and data["last_name"] != "" and data["password"] != "" and data["password2"] != "" and data["phone_no"] != "" and data["aadhar"] != "" and data["pan"] != "" and data["cheque"] != "":
                if len(data['phone_no']) == 10 and re.match("[6-9][0-9]{9}", data['phone_no']):
                    if data['email'] != "" and re.match("^[a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$", data["email"]):  
                        if data["password"] == data["password2"]:
                            user = User.objects.filter(Q(phone_no = data["phone_no"]) | Q(email = data["email"]))
                            if not user:
                                if data["refer_code"] != "":          
                                    try:
                                        referred_user = User.objects.get(refer_code = data["refer_code"])   
                                        data["referred_by"] = referred_user.id                   
                                        data["created_by"] = get_admin.id
                                        data["modified_by"] = get_admin.id
                                        data["under_by"] = get_admin.id
                                        data["tc"] = True
                                        serializer = UserRegistrationSerializer(data=data)
                                        if serializer.is_valid():
                                            serializer.save()
                                            get_user = User.objects.get(id = serializer.data["id"])
                                            # get_user.is_verified = True
                                            get_user.otp_verified = True
                                            get_user.save()
                                            
                                            return onSuccess("User created successfully !!!",serializer.data)
                                        else:
                                            return badRequest("Something Went Wrong !!!")
                                    except:
                                        return badRequest("Invalid referral code or doesn't match !!!")
                                else:
                                    data["created_by"] = get_admin.id
                                    data["modified_by"] = get_admin.id
                                    data["under_by"] = get_admin.id
                                    data["tc"] = True
                                    serializer = UserRegistrationSerializer(data=data)
                                    if serializer.is_valid():
                                        serializer.save()
                                        get_user = User.objects.get(id = serializer.data["id"])
                                        # get_user.is_verified = True
                                        get_user.otp_verified = True
                                        get_user.save()

                                        return onSuccess("User created successfully !!!", serializer.data)
                                    else:
                                        return badRequest("Something Went Wrong !!!")
                            else:
                                return badRequest("User already exists !!!")
                        else:
                            return badRequest("Password and Confirm password doesn't matched !!!")
                    else:
                        return badRequest("Invalid email id, Please try again. !!!")
                else:
                    return badRequest("Invalid mobile number, Please try again. !!!")
            else:
                return badRequest("Fields is missing !!!")   
        else:
            return unauthorisedRequest()
        

#---------------- EDIT USER'S PROFILE (ADMIN ACCESS) -----------------#

class EditUserProfile(APIView):
    
    def patch(self, request):
        if not request.POST._mutable:
            request.POST._mutable = True
        token = get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin= True)
            except:
                return badRequest("Admin not found !!!")  
            data = request.data
            user = User.objects.get(id = data["user_id"]) 
            if user:
                data["modified_by"] = get_admin.id
                data["user_modified_at"] = datetime.now()
                serializer = editUserProfileSerializer(user, data=data, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return onSuccess("Account updated successfully !!!", serializer.data)
                else:
                    return badRequest("Something Went Wrong !!!")
            else:
                return badRequest("User not found !!!")
        else:
            return unauthorisedRequest()     

        
#---------------- DELETE USER (PASS PARAMETER), (ADMIN ACCESS) ------------#

class DeleteUserView(APIView):

    def delete(self, request, format=None):
        token = get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin= True)
            except:
                return badRequest("Admin not found !!!")
            try:
                user_id = request.GET.get("user_id")    
                user = User.objects.get(id=user_id, under_by = get_admin.id)
                user.delete()
                return onSuccess("User Deleted Successfully !!!", 1)
            except:
                return badRequest("User not found !!!")  
        else:
            return unauthorisedRequest()


#--------------------- ADMIN REGISTER API (ADMIN) -------------------------#

@authentication_classes([])
@permission_classes([])
class RegisterAdmin(APIView):
    def post(self, request):
        if not request.POST._mutable:
            request.POST._mutable = True
        data = request.data
        if data["first_name"] != "" and data["last_name"] != "" and data["password"] != "" and data["password2"] != "" and data["phone_no"] != "" :
            if len(data['phone_no']) == 10 and re.match("[6-9][0-9]{9}", data['phone_no']):
                if data['email'] != "" and re.match("^[a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$", data["email"]):  
                    if data["password"] == data["password2"]:
                        user = User.objects.filter(Q(phone_no = data["phone_no"]) | Q(email = data["email"]))
                        if not user:
                            serializer = AdminRegisterSerializer(data=data)
                            if serializer.is_valid():
                                serializer.save()
                                get_user = User.objects.get(id = serializer.data["id"])
                                get_user.created_by = get_user
                                get_user.modified_by = get_user
                                get_user.save()
                                send_otp_via_email(serializer.data['email'])
                                return onSuccess("Registration Successful. Please check your email for verification", serializer.data)
                            else:
                                return badRequest("Something Went Wrong !!!")
                        else:
                            return badRequest("User already exists !!!")
                    else:
                        return badRequest("Password and Confirm password doesn't matched !!!")
                else:
                    return badRequest("Invalid email id, Please try again. !!!")
            else:
                return badRequest("Invalid mobile number, Please try again. !!!")
        else:
            return badRequest("Fields is missing !!!")


#-------------------- VERIFY ADMIN WITH OTP (ADMIN) ------------------------#

@authentication_classes([])
@permission_classes([])
class VerifyAdminOTP(APIView):
    def post(self, request):
        data = request.data
        if data["email"] != "" and data["otp"] != "":
            if len(data["otp"]) == 4:
                serializer = VerifyAccountSerializer(data=data)
                if serializer.is_valid():
                    email = serializer.data['email']
                    otp = serializer.data['otp']

                    user = User.objects.filter(email=email)
                    if not user.exists():
                        return badRequest("User with this Email not Exists !!!")

                    if user[0].otp != otp:
                        return badRequest("Invalid OTP or Doesn't Match !!!")
                    user = user.first()
                    user.otp_verified = True
                    user.is_verified = True
                    user.is_admin = True
                    user.is_staff = True
                    user.save()
                    return onSuccess("Account Verified Successfully !!!", 1)
                else:
                    return badRequest("Something went wrong !!!")
            else:
                return badRequest("Invalid Otp !!!")
        else:
            return badRequest("Fields is missing !!!")


#--------------- ADMIN PROFILE VIEW, UPDATE AND DELETE (ADMIN) ------------#

class AdminProfileView(APIView):
    def get(self,  request):
        token = get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin= True)
            except:
                return badRequest("Admin not found !!!")
            serializer = AdminProfileSerializer(get_admin)
            return onSuccess("Your profile !!!", serializer.data)
        else:
            return unauthorisedRequest()

    def patch(self, request):
        if not request.POST._mutable:
            request.POST._mutable = True
        token= get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin= True)
            except:
                return badRequest("Admin not found !!!") 
            data = request.data
            serializer = AdminProfileSerializer(get_admin, data=data, partial = True)
            if serializer.is_valid():
                get_admin.user_modified_at = datetime.now()
                serializer.save()
                return onSuccess("Your data is updated !!!", serializer.data)
            else:
                return badRequest("Something went wrong !!!")
                # return badRequest(serializer.errors)
        else:
            return unauthorisedRequest()
        
    def delete(self, request):
        token = get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin= True)
                get_admin.delete()
                return onSuccess("Account deleted successfully !!!", 1)
            except :
                return badRequest("Account not found !!!")
        else:
            return unauthorisedRequest()


#---------------------- REGISTRATION (USER) -------------------------#

@authentication_classes([])
@permission_classes([])
class RegisterUser(APIView):

    def post(self, request):
        if not request.POST._mutable:
            request.POST._mutable = True
        data = request.data
        try:
            get_admin = User.objects.get(id= data["id"], is_admin = True)
            print("get admin", get_admin)
        except:
            return badRequest("Admin not found !!!")
        if data["first_name"] != "" and data["last_name"] != "" and data["password"] != "" and data["password2"] != "" and data["phone_no"] != "" and data["aadhar"] != "" and data["pan"] != "" and data["cheque"] != "" and data["tc"] != "":
            if len(data['phone_no']) == 10 and re.match("[6-9][0-9]{9}", data['phone_no']):
                if data['email'] != '' and re.match("^[a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$", data["email"]):
                    if data["password"] == data["password2"]:
                        if data["tc"] == "true":
                            user = User.objects.filter(Q(phone_no = data["phone_no"]) | Q(email = data["email"]))
                            if not user:  
                                if data["refer_code"] != "":          
                                    try:
                                        referred_user = User.objects.get(refer_code = data["refer_code"])   
                                        data["referred_by"] = referred_user.id                   
                                        data["created_by"] = get_admin.id
                                        data["modified_by"] = get_admin.id
                                        data["under_by"] = get_admin.id
                                        serializer = UserRegistrationSerializer(data=data)
                                        if serializer.is_valid():
                                            serializer.save()
                                            send_otp_via_email(serializer.data["email"])
                                            
                                            return onSuccess("Registration Successful. Please check your email for verification", serializer.data)
                                        else:
                                            return badRequest("Something went wrong !!!")
                                    except:
                                        return badRequest("Invalid referral code or doesn't match !!!")
                                else:
                                    data["created_by"] = get_admin.id
                                    data["modified_by"] = get_admin.id
                                    data["under_by"] = get_admin.id
                                    serializer = UserRegistrationSerializer(data=data)
                                    if serializer.is_valid():
                                        serializer.save()
                                        send_otp_via_email(serializer.data['email'])

                                        return onSuccess("Registration Successful. Please check your email for verification", serializer.data)
                                    else:
                                        return badRequest("Something went wrong !!!")
                            else:
                                return badRequest("User already exists !!!")
                        else:
                            return badRequest("Terms and Condition (tc) must be true !!!")
                    else:
                        return badRequest("Password and Confirm password doesn't matched !!!")
                else:
                    return badRequest("Invalid email id, Please try again. !!!")
            else:
                return badRequest("Invalid mobile number, Please try again. !!!")
        else:
            return badRequest("Fields is missing !!!")   


#------------------ VERIFY USER WITH OTP (USER) -----------------------#

@authentication_classes([])
@permission_classes([])
class VerifyUserOTP(APIView):
    def post(self, request):
        data = request.data
        if data["email"] != "" and data["otp"] != "":
            if len(data["otp"]) == 4:
                serializer = VerifyAccountSerializer(data=data)
                if serializer.is_valid():
                    email = serializer.data['email']
                    otp = serializer.data['otp']

                    user = User.objects.filter(email=email)
                    if not user.exists():
                        return badRequest("User with this Email not Exists !!!")

                    if user[0].otp != otp:
                        return badRequest("Invalid OTP or Doesn't Match !!!")

                    user = user.first()
                    user.otp_verified = True
                    user.save()
                    return onSuccess("OTP Verified Successfully !!!", 1)
                else :
                    return badRequest("Something went wrong !!!")
            else:
                return badRequest("Invalid Otp !!!")
        else:
            return badRequest("Fields is missing !!!")


#------------------- USER PROFILE VIEW, UPDATE AND DELETE (USER) ------------------#

class UserProfileView(APIView):
    
    def get(self,  request):
        token = get_object(request)
        if token:
            try:
                get_user = User.objects.get(id = token["user_id"], otp_verified = True)
            except:
                return badRequest("User not found or not otp verified !!!")
            serializer = UserProfileSerializer(get_user)
            return onSuccess("User Profile !!!", serializer.data)
        else:
            return unauthorisedRequest()
    
    def patch(self, request):
        if not request.POST._mutable:
            request.POST._mutable = True
        token= get_object(request)
        if token:
            try:
                get_user = User.objects.get(id = token["user_id"], otp_verified = True)
            except:
                return badRequest("User not found !!!") 
            data = request.data
            serializer = UserProfileSerializer(get_user, data=data, partial = True)
            if serializer.is_valid():
                get_user.user_modified_at = datetime.now()
                get_user.modified_by = get_user
                serializer.save()
                return onSuccess("Your data is updated !!!", serializer.data)
            else:
                return badRequest("Something went wrong !!!")
                # return badRequest(serializer.errors)
        else:
           return unauthorisedRequest()

    def delete(self, request):
        token = get_object(request)
        if token:
            try:
                get_user = User.objects.get(id = token["user_id"], otp_verified = True)
                get_user.delete()
                return onSuccess("Account deleted successfully !!!", 1)
            except:
                return badRequest("Account not found !!!")
        else:
            return unauthorisedRequest()


#---------------------- LOGIN USER (ADMIN, USER) -------------------------#

@authentication_classes([])
@permission_classes([])
class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        if data["email"] != "" and data["password"] != "":
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data.get('email')
                password = serializer.data.get('password') 
                user = authenticate(email=email, password=password) 
                if user is not None and user.otp_verified:
                    token=  get_tokens_for_user(user)
                    return onSuccess("Login successful !!!", {"token": token})
                elif user is None:
                    return badRequest("Invalid credentials !!!") 
                else:
                    send_otp_via_email(serializer.data['email']) 
                    return badRequest("You are not a verified user!!! Please check your email and get verified.")
            else:      
                return badRequest("Something went wrong !!!")
                # return Response({"Status":False, "Data":serializer.errors})
        else:
            return badRequest("Fields is missing !!!")


#------------------ RESEND OTP (ADMIN, USER) -----------------------------#

@authentication_classes([])
@permission_classes([])
class ResendOTP(APIView):
    def post(self, request):
        data = request.data
        if data["email"] != "":
            serializer = ResendOTPSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                user = User.objects.filter(email=email)
                if not user.exists():
                    return badRequest("Invalid Email or not Exists !!!")
                send_otp_via_email(serializer.data['email'])  
                return onSuccess("Please check your email again !!!", 1)
            else:
                return badRequest("Something went wrong !!!")
        else:
            return badRequest("Field is missing !!!")


#------------------- CHANGE PASSWORD VIEW (ADMIN, USER) ---------------------#

class UserChangePasswordView(APIView):
    def post(self, request, format=None):
        token = get_object(request)
        if token:
            data = request.data
            if data["old_password"] != "" and data["password"] != "" and data["password2"] != "":
                if data["password"] == data["password2"]:
                    get_user = User.objects.get(id= token["user_id"])
                    if get_user and get_user.is_verified:    
                        user_password = get_user.password
                        old_password= data["old_password"]
                        checkPass = check_password(old_password, user_password)
                        if checkPass:
                            get_user.set_password(data["password"])
                            get_user.save()
                            return onSuccess("Password changed successfully !!!", 1)
                        else:
                            return badRequest("Old password doesn't match !!!")
                    else:
                        return badRequest("user not found")
                else:
                    return badRequest("Password and confirm password doesn't matched !!!")
            else:
                return badRequest("Fields is missing !!!")
        else:
            return unauthorisedRequest()


#---------------- SEND RESET PASSWORD EMAIL (ADMIN, USER) ------------------#

@authentication_classes([])
@permission_classes([])
class SendResetPasswordEmail(APIView):

    def post(self, request):
        data = request.data
        if data["email"] != "":
            serializer = ResetPasswordEmailSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                user = User.objects.filter(email=email)
                if not user.exists():
                    return badRequest("Invalid Email or not exists !!!")
                send_reset_password_otp_via_email(serializer.data['email']) 
                return onSuccess("Please check your email !!!", 1)
            else:
                return badRequest("Something went wrong !!!")
        else:
            return badRequest("Field is missing !!!")

 
#------------------- VERIFY RESET PASSWORD EMAIL (ADMIN, USER) ----------------#

@authentication_classes([])
@permission_classes([])
class VerifyResetPasswordOTPView(APIView):
    def post(self, request):
        data = request.data
        if data["email"] != "" and data["otp"] != "":
            if len(data["otp"]) == 4:
                serializer = VerifyPasswoprdOTPSerializer(data=data)
                if serializer.is_valid():
                    email = serializer.data['email']
                    otp = serializer.data['otp']
                    user = User.objects.filter(email=email)
                    if not user.exists():
                        return badRequest("Invalid Email or doesn't exists !!!")
                    if user[0].otp != otp:
                        return badRequest("Invalid OTP or Doesn't Match !!!")
                    return onSuccess("OTP verified successfully !!!", 1)
                else:
                    return badRequest("Something went wrong !!!")
            else:
                return badRequest("Invalid Otp !!!")
        else:
            return badRequest("Field is missing !!!")


#---------------------- RESET PASSWORD (ADMIN, USER) ------------------------#

@authentication_classes([])
@permission_classes([])
class PasswordResetView(APIView):
    def post(self, request,  format=None):
        data = request.data
        if data["email"] != "" and data["password"] != "" and data["password2"] != "":
            if data["password"] == data["password2"]:
                get_user = User.objects.get(email = data["email"])
                if get_user:
                    get_user.set_password(data["password"])
                    get_user.save()
                    return onSuccess("Password Reset Successfully !!!", 1)
                else:
                    return badRequest("User not found !!!")
            else:
                return badRequest("password and confirm password doesn't match !!!")            
        else:
            return badRequest("Fields is missing !!!")

























