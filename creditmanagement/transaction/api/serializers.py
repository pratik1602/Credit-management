from rest_framework import serializers
from usercredit.models import *

# class RecordSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Transaction
#         fields = "__all__"

# class RequestDetailsSerializer(serializers.ModelSerializer):
#     # payment_status = serializers.BooleanField()

#     class Meta:
#         model = Payment_Request
#         fields = ["payment_status"]

#---------------------- ADD PAYMENT RECORD SERIALIZER --------------------#

#---------------------------- SERIALIZER FOR DEPOSIT METHOD --------------#
class UserCardDepositPaymentSerializer(serializers.ModelSerializer):
    deposit_charges = serializers.FloatField(required = False)
    profit = serializers.FloatField(required = False)
    # payment_status = serializers.BooleanField()

    class Meta:
        model = Transaction
        fields = ["transaction_id","admin","card", "user", "payment_request", "paid_amount", "payment_type", "due_paid_through", "deposit_charges", "profit"]

#-------------------------- SERIALIZER FOR CYCLE METHOD ------------------#
class UserCardCycleandWithdrawPaymentSerializer(serializers.ModelSerializer):
    deposit_charges = serializers.FloatField(required = False)
    withdraw_charges = serializers.FloatField(required = False)
    profit = serializers.FloatField(required = False)
    payment_method_flag = serializers.CharField(required = False)
    # payment_status = serializers.BooleanField()

    class Meta:
        model = Transaction
        fields = ["transaction_id","admin","card", "user", "payment_request", "paid_amount", "payment_type", "due_paid_through", "deposit_charges", "profit", "withdraw_charges", "payment_method_flag"] 


class CardDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ['user_id','card_id','card_number', 'card_bank_name', 'card_holder_name', 'commission']

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "profile_pic"]

class PaymentRequestdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_Request
        fields = ['request_id', 'due_amount', 'due_date', 'payment_method', 'payment_status',  'cycle_deposit_status', 'cycle_withdraw_status']

class AllTransactionRecordSerializer(serializers.ModelSerializer):
    card = CardDetailsSerializer()
    user = UserDetailsSerializer()
    payment_request = PaymentRequestdetailsSerializer()
    charge_sum = serializers.FloatField(write_only= True)

    class Meta:
        model = Transaction
        fields = ["transaction_id","admin","user", "card", "payment_request","due_paid_at", "paid_amount",  "payment_type", "due_paid_through", "deposit_charges", "withdraw_charges", "profit", "profit_amount", "withdraw_amount", "total_amount", "payment_received", 'payment_method_flag', 'charge_sum']

class EditTransactionRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["transaction_id", "payment_received"]


#---------------------- DASHBOARD VIEWS DATA SERIALIZER ------------------------#

#--------- GRAPH 2 ------------#

class TranactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["paid_amount",  "payment_type", "payment_method_flag","deposit_charges", "withdraw_charges","withdraw_amount", "profit", "profit_amount", "due_paid_at" ]

class PaidUnpaidWithdrawSerializer(serializers.ModelSerializer):
    paid_amount =serializers.SerializerMethodField()
    @staticmethod
    def get_paid_amount(obj):
        amount = Transaction.objects.filter(payment_request = obj.request_id)
        paid_amount = TranactionDetailsSerializer(amount, many= True)
        return paid_amount.data
        
    class Meta:
        model = Payment_Request 
        fields = ['request_id','payment_method', 'payment_status', 'due_amount', 'paid_amount']

#----------- GRAPH 1 & 3 ---------------#

class CardsCountsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ['card_id']

class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_Request
        fields = ['request_id', 'due_amount', 'due_date', 'payment_method', 'payment_status']

class ProfitUnpaidProfitDetailsSerializer(serializers.ModelSerializer):
    card = CardsCountsSerializer()
    payment_request = PaymentRequestdetailsSerializer()

    class Meta:
        model = Transaction
        fields = ["card", "payment_request","due_paid_at", "paid_amount",  "payment_type", "due_paid_through", "deposit_charges", "profit", "profit_amount", "withdraw_amount", "payment_received"]



# #-------------------------- GENERATE PDF SERIALIZER ----------------------------#

# class GeneratePdfSerializer(serializers.ModelSerializer):
#     class Meta:
#         Model = Transaction
#         fields = ["pdf"]