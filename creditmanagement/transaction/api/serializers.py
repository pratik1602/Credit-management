from rest_framework import serializers
from usercredit.models import *

# class RecordSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Transaction
#         fields = "__all__"

#---------------------- ADD PAYMENT RECORD SERIALIZER --------------------#

class UserCardPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["transaction_id","admin","card", "due_paid_date","due_paid_time", "paid_amount", "due_paid_through"]


class CardDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ['user_id','card_id','card_number', 'card_bank_name', 'card_holder_name', 'commission']

class AllTransactionRecordSerializer(serializers.ModelSerializer):
    card = CardDetailsSerializer()

    class Meta:
        model = Transaction
        fields = ["transaction_id","admin","card","due_paid_date","due_paid_time", "paid_amount", "due_paid_through", "user"]

class EditTransactionRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["transaction_id", "due_paid_date","due_paid_time", "paid_amount", "due_paid_through"]
