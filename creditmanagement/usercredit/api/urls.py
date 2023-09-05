from django.contrib import admin
from django.urls import  path

from usercredit.api.views import *

urlpatterns = [

    #------------------------------ REGISTRATION ----------------------------# 

    #---- USER REGISTER
    path('user-register', RegisterUser.as_view(), name= "RegisterUser"),

    #---- ADMIN REGISTER 
    path ('register-admin', RegisterAdmin.as_view(), name="RegisterAdmin"),


    #------------------------------ VERIFICATION -----------------------------#

    #---- VERIFY USER
    path('verify-user-otp', VerifyUserOTP.as_view(), name="VerifyUserOTP"),

    #---- RESEND OTP
    path('resend-otp', ResendOTP.as_view(), name="ResendOTP"),


    #----------------------------- USER PROFILE ------------------------------#

    path ('user-profile', UserProfileView.as_view(), name="UserProfileView"),
    path ('edit-profile', UserProfileView.as_view(), name="UserProfileView"),
    path ('delete-profile', UserProfileView.as_view(), name="UserProfileView"),


    #---------------------------- ADMIN PROFILE ------------------------------#

    path ('admin-profile', AdminProfileView.as_view(), name="AdminProfileView"),
    path ('admin-edit-profile', AdminProfileView.as_view(), name="AdminProfileView"),
    path ('admin-delete-profile', AdminProfileView.as_view(), name="AdminProfileView"),


    #-------------------------------- LOGIN -----------------------------------#

    #---- LOGIN USER 
    path('login-user', LoginAPIView.as_view(), name="LoginAPIView"),

    #---- LOGIN ADMIN 
    path('login-admin', LoginAPIView.as_view(), name="LoginAPIView"),

    #---- VERIFY ADMIN WITH OTP (ADMIN)
    path('verify-admin', VerifyAdminOTP.as_view(), name="VerifyAdminOTP"),



    #-------------------------- CHANGE PASSWORD -----------------------------#

    #---- CHANGE PASSWORD (ADMIN, USER)
    path ('change-password', UserChangePasswordView.as_view(), name="UserChangePasswordView"),


    #----------------------- RESET PASSWORD (ADMIN, USER) -------------------#
    
    #---- SEND RESET PASSWORD OTP 
    path('reset-password-email', SendResetPasswordEmail.as_view(), name="SendResetPasswordEmail"),

    #---- VERIFY RESET PASSWORD OTP 
    path('verify-Reset-pass-OTP', VerifyResetPasswordOTPView.as_view(), name="VerifyResetPasswordOTPView"),

    #---- SET RESET PASSWORD 
    path('reset-password', PasswordResetView.as_view(), name="PasswordResetView"),


    #----------------------------- ADMIN ACCESSES -----------------------------# 

    #----  USER'S LIST VIEW (ADMIN ACCESS)
    path ('user-list', GetUserList.as_view(), name="GetUserList"),

    #---- DELETE USER'S ACCOUNT (ADMIN ACCESS)
    path ('admin-delete-user', DeleteUserView.as_view(), name="DeleteUserView"),

    #---- CREATE USER'S ACCOUNT (ADMIN ACCESS)
    path('create-account', CreateUserAccount.as_view(), name="CreateUserAccount"),

    #---- VERIFY USER'S ACCOUNT (ADMIN ACCESS)
    path('verify-account', VerifyUserAccount.as_view(), name="VerifyUserAccount"),

    #---- EDIT USER'S PROFILE (ADMIN ACCESS)
    path('edit-user-profile', EditUserProfile.as_view(), name="EditUserProfile"),

    #--- Admin notification
    path('admin-notification' , websocket.as_view() , name='websocket'),
    
]