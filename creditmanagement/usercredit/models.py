from django.db import models
from django.contrib.auth.models import  AbstractBaseUser
from core.cardValidate import *
from usercredit.manager import *
from django.core.validators import MaxValueValidator, MinValueValidator
percentage_validators=[MinValueValidator(0), MaxValueValidator(100)]
from django.conf import settings
from usercredit.utils import *
from django.contrib.auth.models import PermissionsMixin
import uuid
from datetime import date
from datetime import time

#------------------ USER MODEL (ADMIN, USERS) -------------------#

class User(AbstractBaseUser,PermissionsMixin):

    ADMIN = 1
    USER = 2

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (USER, 'User'),
    )   

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    username = None
    profile_pic =  models.ImageField(upload_to="Images\Profile_pic", default="")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=12)
    aadhar = models.ImageField(upload_to= "Images\Aadhar", default="")
    # aadhar_status = models.BooleanField(default=False)
    pan = models.ImageField(upload_to= "Images\Pan", default="")
    # pan_status = models.BooleanField(default=False)
    cheque = models.ImageField(upload_to= "Images\Cheque", default="")
    # cheque_status = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=2)
    is_verified = models.BooleanField(default=False)
    is_active =  models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False)
    tc = models.BooleanField(default=False)
    otp = models.CharField(max_length=6)
    otp_verified = models.BooleanField(default=False)
    refer_code = models.CharField(max_length=8, blank=True, null=True)
    referred_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='usercredit_User_referred_by')
    commission_status = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='usercredit_User_created_by')
    modified_by =  models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='usercredit_User_modified_by')
    user_created_at = models.DateTimeField(default=datetime.now)
    user_modified_at = models.DateTimeField(default=datetime.now)
    under_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='usercredit_User_under_by')
    
    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_no', ]

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def  has_module_perms(self, app_label):
        return self.is_admin

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.refer_code == "":
            refer_code = generate_ref_code()
            self.refer_code = refer_code
        super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        try:
            old_profile_pic = User.objects.get(id=self.id)
            if old_profile_pic.profile_pic != self.profile_pic:
                old_profile_pic.profile_pic.delete()
        except: pass
        super(User, self).save(*args, **kwargs)


#----------------------------- CARDS MODEL (ADMIN, USERS) -----------------------#

class Card(models.Model):  

    card_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # CARD_CHOICE = (("business", "BUSINESS"),
    #             ("personal", "PERSONAL"),)
    card_bank_name = models.CharField(max_length=100)
    # card_type = models.CharField(max_length=20)
    card_category = models.CharField(max_length=20, blank = True)
    card_network = models.CharField(max_length=50)
    card_number = models.PositiveBigIntegerField( unique=True) #validators=[validate_card_number],
    card_holder_name= models.CharField(max_length=100)
    frontside_card_photo = models.ImageField(upload_to= "Images\Cards\FrontSide", default="")
    backside_card_photo = models.ImageField(upload_to= "Images\Cards\BackSide", default="")
    card_exp_date = models.DateField() #validators=[is_expired]
    card_cvv = models.IntegerField() #validators=[validate_cvv]
    commission = models.FloatField(validators=percentage_validators, blank=True, null=True, default=2.0, editable=True)
    # card_status = models.BooleanField(default=False)
    updated_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_by_user', on_delete=models.SET_NULL,  null=True, blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_by_user',on_delete=models.SET_NULL,  null=True, blank=True)
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='paid_by_user', on_delete=models.SET_NULL, null=True, blank=True) 
    commission_paid_through = models.CharField(max_length=100, blank= True, null= True)
    created_at = models.DateTimeField(default= datetime.now)
    modified_at = models.DateTimeField(default=datetime.now)
    available_balance = models.FloatField(default=0, blank= True)
    credit_amount = models.FloatField(default=0, blank= True)

    def __str__(self):
        return self.card_bank_name      

#---------------------------------- PAYMENT REQUEST MODEL ---------------------------#

class Payment_Request(models.Model):

    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name="payment_admin_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name="payment_user_id")
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, related_name="requested_card_id")
    payment_method = models.CharField(max_length=25)
    due_amount = models.FloatField(default=0, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True) #validators=[has_expired]
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requested_by_user',on_delete=models.SET_NULL,  null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    cycle_deposit_status = models.BooleanField(default=False)
    cycle_withdraw_status = models.BooleanField(default=False)
    requested_at = models.DateTimeField(default= datetime.now)
    modified_at = models.DateTimeField(default=datetime.now)

    def __str__(self) :
            return self.payment_method

#-------------------------------- TRANSACTION MODEL ------------------------------#

class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name="admin_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name="user_id")
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, related_name="user_card_id")
    payment_request = models.ForeignKey(Payment_Request, on_delete=models.SET_NULL, null=True, related_name="payment_request_id")
    due_paid_through = models.CharField(max_length=100)
    paid_amount = models.FloatField(default=0, blank=True, null=True)
    due_paid_at = models.DateTimeField(default= datetime.now)
    payment_type = models.CharField(max_length=30)
    deposit_charges = models.FloatField(default=0, blank=True, null=True)
    withdraw_charges = models.FloatField(default=0, blank=True, null=True)
    withdraw_amount = models.FloatField(null=True,blank=True)
    payment_method_flag = models.CharField(max_length=25, blank= True, null= True)
    # commission = models.FloatField(validators=percentage_validators, blank=True, null=True, default=0, editable=True)
    profit = models.FloatField(validators=percentage_validators, blank=True, null=True, default=0, editable=True)
    profit_amount = models.FloatField(null=True,blank=True)
    total_amount = models.FloatField(null=True,blank=True)
    payment_received = models.BooleanField(default=False)
    pdf = models.FileField(upload_to= "Pdf/UserPdf", default="")
    
    def __str__(self) :
        return self.due_paid_through



