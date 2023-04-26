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
        fields = ["transaction_id","admin","card", "payment_type", "paid_amount", "due_paid_through", "charges"]


class CardDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ['user_id','card_id','card_number', 'card_bank_name', 'card_holder_name', 'commission']

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "profile_pic"]

class AllTransactionRecordSerializer(serializers.ModelSerializer):
    card = CardDetailsSerializer()
    user = UserDetailsSerializer()

    class Meta:
        model = Transaction
        fields = ["transaction_id","admin","user", "card","due_paid_at", "paid_amount", "due_paid_through", "charges"]

class EditTransactionRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["transaction_id", "due_paid_date","due_paid_time", "paid_amount", "due_paid_through"]
