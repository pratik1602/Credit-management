from rest_framework import serializers
from usercredit.models import *
from usercredit.api.serializers import *


#-------------------- USER'S CARD SERIALIZER ------------------------#

class UserCardSerializer(serializers.ModelSerializer):
    # card_number = serializers.IntegerField(read_only = True)
    commission = serializers.FloatField(required=False)

    class Meta:
        model = Card
        fields = ['card_id','card_bank_name', 'card_category' ,'card_number','card_network','card_holder_name' ,'frontside_card_photo', 'backside_card_photo','card_exp_date' ,'card_cvv','commission']

#--------------------CREATE AND UPDATE USER'S CARD SERIALIZER ------------------------#

class CreateUpdateUserCardSerializer(serializers.ModelSerializer):
    # due_date = serializers.DateTimeField(required = False)
    # due_amount = serializers.FloatField(required = False)
    class Meta:
        model = Card
        fields = ['card_id','card_bank_name', 'card_category' ,'card_number','card_network','card_holder_name' ,'frontside_card_photo', 'backside_card_photo','card_exp_date' ,'card_cvv','commission'] 


#---------------------- USER'S PROFILE SERIALIZER -------------------#

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id","profile_pic","first_name", "last_name", "under_by"]

#------------------------- USERS CARDS SERIALIZER --------------------#

class AllCardSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    class Meta:
        model = Card
        # fields = "__all__"
        fields = ['card_id',"user_id",'card_bank_name','card_type', 'card_category', 'card_number','card_network','card_holder_name' ,'frontside_card_photo', 'backside_card_photo','card_exp_date' ,'card_cvv', 'commission']

#------------------------- ADMIN CARDS SERIALIZER ---------------------#

# class AdminDebitCardSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Card
#         fields = ['user_id','card_id','card_number', 'card_bank_name', 'card_holder_name', 'available_balance', 'card_type', 'card_photo', 'card_exp_date', 'card_cvv', 'card_network']
    
class AdminCreditCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ['user_id','card_id','card_number', 'card_bank_name', 'card_holder_name',  'card_category' , 'frontside_card_photo', 'backside_card_photo', 'card_exp_date', 'card_cvv', 'card_network', 'credit_amount']
    
class AdminAllcardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ['user_id','card_id','card_number', 'card_bank_name', 'card_holder_name', 'card_type',  'card_category' , 'frontside_card_photo', 'backside_card_photo', 'card_exp_date', 'card_cvv', 'card_network', 'credit_amount', 'available_balance']








