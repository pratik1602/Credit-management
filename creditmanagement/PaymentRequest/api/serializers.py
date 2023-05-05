from rest_framework import serializers
from usercredit.models import *
# from usercredit.api.serializers import *

#------------------- ADD PAYMENT REQUEST SERIALIZER (ADMIN, USER) ----------------#

class AddPaymentRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment_Request
        fields = ['request_id', 'payment_method','due_amount', 'due_date', 'card', 'user', 'admin', 'requested_by']

#------------------ GET PAYMENT REQUEST (ADMIN, USER) -------------------------#

class CardDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ['card_id','card_bank_name', 'card_category' ,'card_number','card_network','card_holder_name' ,'card_photo','card_exp_date' ,'card_cvv','commission']

class GetPaymentRequestSerializer(serializers.ModelSerializer):
    card = CardDetailSerializer()

    class Meta:
        model = Payment_Request
        fields = ['request_id', 'card','due_amount', 'due_date', 'payment_method', 'payment_status', 'cycle_deposit_status', 'cycle_withdraw_status']