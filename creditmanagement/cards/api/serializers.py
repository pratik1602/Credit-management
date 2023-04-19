from rest_framework import serializers
from usercredit.models import *
from usercredit.api.serializers import *


#-------------------- USER'S CARD SERIALIZER ------------------------#

class UserCardSerializer(serializers.ModelSerializer):
    # card_number = serializers.IntegerField(read_only = True)
    # commission = serializers.FloatField(read_only=True)

    class Meta:
        model = Card
        fields = ['card_id','card_bank_name', 'card_category' ,'card_number','card_network','card_holder_name' ,'card_photo','card_exp_date' ,'card_cvv','commission','due_date','due_amount']
    

#---------------------- USER'S PROFILE SERIALIZER -------------------#

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "profile_pic", "under_by"]

#------------------------- USERS CARDS SERIALIZER --------------------#

class AllCardSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    class Meta:
        model = Card
        # fields = "__all__"
        fields = ['card_id',"user_id",'card_bank_name','card_type', 'card_category', 'card_number','card_network','card_holder_name' ,'card_photo','card_exp_date' ,'card_cvv','due_date','due_amount', 'card_status', 'commission', 'profit_amount','updated_by', 'created_by', 'paid_by', 'created_at', 'modified_at']

#------------------------- ADMIN CARDS SERIALIZER ---------------------#

class AdminDebitCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ['user_id','card_id','card_number', 'card_bank_name', 'card_holder_name', 'available_balance', 'card_type', 'card_photo', 'card_exp_date', 'card_cvv', 'card_network']
    
class AdminCreditCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ['user_id','card_id','card_number', 'card_bank_name', 'card_holder_name', 'card_type',  'card_category' , 'card_photo', 'card_exp_date', 'card_cvv', 'card_network', 'credit_amount']
    
class AdminAllcardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ['user_id','card_id','card_number', 'card_bank_name', 'card_holder_name', 'card_type',  'card_category' , 'card_photo', 'card_exp_date', 'card_cvv', 'card_network', 'credit_amount', 'available_balance']


#---------------------- ADD PAYMENT RECORD SERIALIZER --------------------#

class UserCardPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["transaction_id","admin","card", "due_paid_date","due_paid_time", "paid_amount", "due_paid_through"]





