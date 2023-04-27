from rest_framework.response import Response
from usercredit.models import *
from PaymentRequest.api.serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from core.decode import get_object
from datetime import datetime
from core.response import *
from django.db.models import Q

#------- YOUR VIEWS ----------#

#------------------------ GET ALL PAYMEMT REQUEST (ADMIN ACCESS) ------------------#

class GetPaymentRequest(APIView):
    def get(self, request):
        token =  get_object(request)
        if token:    
            try:
                get_admin = User.objects.get(id = token["user_id"])
            except:
                return badRequest("Admin not found !!!")
            request_id = request.GET.get("request_id")
            card_id = request.GET.get("card_id")
            if request_id != None or 0:
                try:
                    payment_request_obj = Payment_Request.objects.get(request_id = request_id)
                    serializer =  GetPaymentRequestSerializer(payment_request_obj)
                    return onSuccess("Payment Request Object !!!", serializer.data)
                except:
                    return badRequest("No Request found !!!")
            elif card_id != None or 0:
                payment_request_objs = Payment_Request.objects.filter(card__card_id = card_id)
                if payment_request_objs:
                    serializer = GetPaymentRequestSerializer(payment_request_objs, many = True)
                    return onSuccess("Payment Request Objects with Card !!!", serializer.data)
                else:
                    serializer = GetPaymentRequestSerializer(payment_request_objs, many = True)
                    return onSuccess("Payment Request Objects with Card !!!", serializer.data)
            else:
                all_payment_request_objs = Payment_Request.objects.filter(admin = get_admin)
                if all_payment_request_objs:
                    serializer = GetPaymentRequestSerializer(all_payment_request_objs, many=True)
                    return onSuccess("All Payment Request Objects !!!",  serializer.data)
                else:
                    serializer = GetPaymentRequestSerializer(all_payment_request_objs, many=True)
                    return onSuccess("All Payment Request Objects !!!",  serializer.data)
        else:
            return unauthorisedRequest()



#--------------------- ADD PAYMENT REQUEST BY ADMIN ---------------------#

class AddPaymentRequestByAdmin(APIView):
    def post(self, request):
        token = get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"])
            except:
                return badRequest("Admin not found !!!")
            data = request.data
            if data["payment_method"] != "" and data["due_amount"] != "" and data["due_date"] != "":
                try:
                    get_card = Card.objects.get(card_id = data["card_id"], user_id__under_by = get_admin)
                    print("get card", get_card)
                except:
                    return badRequest("Card not found !!!")
                
                data["user"] = get_card.user_id.id 
                data["card"] = get_card.card_id
                data["admin"] = get_admin.id
                data["requested_by"] = get_admin.id

                serializer = AddPaymentRequestSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    get_requested_obj = Payment_Request.objects.get(request_id = serializer.data["request_id"])
                    get_requested_obj.save() 
                    return onSuccess("Payment Request Added Successfully !!!", serializer.data)
                else:
                    # return badRequest(serializer.errors)
                    return badRequest("Something went wrong !!! ")
            else:
                return badRequest("Fields is missing !!!")
        else:
            return unauthorisedRequest()
        
#--------------------- ADD PAYMENT REQUEST BY USER ---------------------#

class AddPaymentRequestByUser(APIView):
    def post(self, request):
        token = get_object(request)
        if token:
            try:
                get_user = User.objects.get(id = token["user_id"])
            except:
                return badRequest("User not found !!!")
            data = request.data
            if data["payment_method"] != "" and data["due_amount"] != "" and data["due_date"] != "":
                try:
                    get_card = Card.objects.get(card_id = data["card_id"], user_id = get_user)
                    print("get card", get_card)
                except:
                    return badRequest("Card not found !!!")
                
                data["user"] = get_card.user_id.id 
                data["card"] = get_card.card_id
                data["admin"] = get_card.user_id.under_by.id
                data["requested_by"] = get_user.id

                serializer = AddPaymentRequestSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    get_requested_obj = Payment_Request.objects.get(request_id = serializer.data["request_id"])
                    get_requested_obj.save() 
                    return onSuccess("Payment Request Added Successfully !!!", serializer.data)
                else:
                    # return badRequest(serializer.errors)
                    return badRequest("Something went wrong !!! ")
            else:
                return badRequest("Fields is missing !!!")
        else:
            return unauthorisedRequest()