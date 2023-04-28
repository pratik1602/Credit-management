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

class UserCardPaymentSerializer(serializers.ModelSerializer):
    charges = serializers.FloatField(required = False)
    commission = serializers.FloatField(required = False)
    # payment_status = serializers.BooleanField()

    class Meta:
        model = Transaction
        fields = ["transaction_id","admin","card", "user", "payment_request", "paid_amount", "payment_type", "due_paid_through", "charges", "commission"]


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
        fields = ['request_id', 'due_amount', 'due_date', 'payment_method', 'payment_status']

class AllTransactionRecordSerializer(serializers.ModelSerializer):
    card = CardDetailsSerializer()
    user = UserDetailsSerializer()
    payment_request = PaymentRequestdetailsSerializer()

    class Meta:
        model = Transaction
        fields = ["transaction_id","admin","user", "card", "payment_request","due_paid_at", "paid_amount",  "payment_type", "due_paid_through", "charges", "commission", "profit_amount", "payment_received"]

class EditTransactionRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["transaction_id", "payment_received"]
