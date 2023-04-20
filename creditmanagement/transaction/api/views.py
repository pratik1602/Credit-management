from usercredit.models import *
from rest_framework.response import Response
from transaction.api.serializers import *
from core.emails import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from core.decode import get_object
from usercredit.utils import *
from core.response import *
from datetime import datetime
from django.contrib.auth.hashers import check_password


#------------- GET, UPDATE AND DELETE PAYMENT RECORDS (ADMIN ACCESS) ------------#

class PaymentRecords(APIView):
    def get(self, request):
        token = get_object(request)
        if token:
            get_admin = User.objects.get(id = token["user_id"])
            if get_admin and get_admin.is_admin:
                transaction_id = request.GET.get("transaction_id")
                user_id = request.GET.get("user_id")
                card_id = request.GET.get("card_id")
                if transaction_id != None or 0:
                    try:
                        record_obj = Transaction.objects.get(transaction_id = transaction_id)
                        serializer = AllTransactionRecordSerializer(record_obj)
                        return onSuccess("Transaction Record !!!", serializer.data)
                    except:
                        return badRequest("No records found !!!")
                    
                elif user_id != None or 0:
                    try:
                        get_user = User.objects.get(id = user_id)
                    except:
                        return badRequest("User not found !!!")
                    record_objs = Transaction.objects.filter(user = get_user)
                    if record_objs.exists():
                        serializer = AllTransactionRecordSerializer(record_objs, many = True)
                        return onSuccess("User's all transactions !!!", serializer.data)
                    else:
                        serializer = AllTransactionRecordSerializer(record_objs, many = True)
                        return onSuccess("No Transactions found for user !!!", serializer.data)
                    
                elif card_id != None or 0:
                    record_objs = Transaction.objects.filter(card__card_id = card_id)
                    if record_objs:
                        serializer = AllTransactionRecordSerializer(record_objs, many = True)
                        return onSuccess("Records with Card number !!!", serializer.data)
                    else:
                        serializer = AllTransactionRecordSerializer(record_objs, many = True)
                        return onSuccess("No Records found with given Card number !!!", serializer.data)
                    
                else:
                    all_records_objs = Transaction.objects.filter(admin = get_admin)
                    if all_records_objs:
                        serializer = AllTransactionRecordSerializer(all_records_objs, many=True)
                        return onSuccess("Records List !!!",  serializer.data)
                    else:
                        serializer = AllTransactionRecordSerializer(all_records_objs, many=True)
                        return onSuccess("Records List !!!",  serializer.data)
            else:
                return badRequest("Admin not found !!!")
        else:
            return unauthorisedRequest()

             
#------------------ TRANSACTIONS RECORD CRUD ---------------------------#

class UserCardPayemtRecord(APIView):
    def post(self, request):
        token = get_object(request)
        if token:
            get_admin = User.objects.get(id = token["user_id"])
            if get_admin and get_admin.is_admin:
                data = request.data
                if data["card"] != "" and data["paid_amount"] != "" and data["due_paid_date"] != "" and data["due_paid_time"] != "" and data["due_paid_through"] != "": 
                    try:
                        card_obj = Card.objects.get(card_id = data["card"])
                    except:
                        return badRequest("Card doesn't exists !!!")
                    data["card"] = card_obj.card_id
                    data["admin"] = get_admin.id
                    serializer = UserCardPaymentSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        get_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                        get_record.user = card_obj.user_id
                        get_record.save()
                        return onSuccess("Payment record added successfully !!!", serializer.data)
                    else:
                        return badRequest("Something went wrong !!!")  
                else:
                    return badRequest("Fields is missing !!!")
            else:
                return  badRequest("Admin not found !!!")
        else:
            return unauthorisedRequest()

class UpdateDeleteTransactionRecord(APIView):
    def patch(self, request):
        token = get_object(request)
        if token:
            get_admin = User.objects.get(id = token["user_id"])
            if get_admin and get_admin.is_admin:
                data = request.data
                if data["due_paid_through"] != "" and data["paid_amount"] != "" and data["due_paid_date"] != "" and data["due_paid_time"] != "":
                    try:
                        get_transaction = Transaction.objects.get(transaction_id = data["transaction_id"])
                    except:
                        return badRequest("No Record found !!!")
                    serializer = EditTransactionRecordSerializer(get_transaction, data=data, partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        return onSuccess("Record Updated Successfully !!!", serializer.data)
                    else:
                        return badRequest("Something went wrong !!!")
                else:
                    return badRequest("Fields is missing !!!")
            else:
                return badRequest("Admin not found !!!")
        else:
            return unauthorisedRequest()
        
    def delete(self, request):
        token = get_object(request)
        if token:
            get_admin = User.objects.get(id = token['user_id'])
            if get_admin and get_admin.is_admin:
                transaction_id = request.GET.get("transaction_id") 
                try:
                    get_record = Transaction.objects.get(transaction_id = transaction_id)
                    get_record.delete()
                    return onSuccess("Record deleted successfully !!!", 1)
                except:
                    return badRequest("Record not found !!!")
            else:
                return badRequest("Admin not found !!!")
        else:
            return unauthorisedRequest()









# class PaymentRecord(APIView):
#     permission_classes = [IsAuthenticated&IsAdminUser]

#     def post(self, request):
#         admin = get_object(request)
#         request.data["user_id"] = admin
#         get_admin = User.objects.get(id = admin.id)
#         if get_admin:
#             data = request.data
#             try:
#                 get_card_id = data["card"]
#                 get_card = Card.objects.get(card_id = get_card_id)
#                 print("get_card", get_card)
#             except:
#                 return Response({"Status":False, "Message":"Card not found !!!"})
#             serializer = RecordSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 get_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
#                 Total_profit_amount =  get_record.amount_paid * get_record.commission/100 
#                 get_record.profit_amount = "%.2f" % float(Total_profit_amount)
#                 get_record.card = get_card
#                 get_record.admin = get_admin
#                 get_record.save()
#                 return Response({"Status":True, "Message":"Record Added Successfully !!!"})
#             else:
#                 return Response({"Status":False, "Data":serializer.errors})
#         else:
#             return Response({"Status":False, "Message":"Admin not found !!!"})
        
#     def put(self, request):
#         admin = get_object(request)
#         request.data["user_id"] = admin
#         get_admin = User.objects.get(id = admin.id)
#         if get_admin:
#             try:
#                 data = request.data
#                 get_record = Transaction.objects.get(transaction_id = data["transaction_id"])
#                 serializer = RecordSerializer(get_record, data=data)   
#                 if serializer.is_valid(): 
#                     serializer.save()
#                     get_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
#                     get_record.profit_amount = get_record.amount_paid * get_record.commission/100
#                     get_record.save()
#                     return Response({"Status":True, "Message":"Record Updated successfully !!!"})
#                 else:
#                     return Response({"Status":False, "Data":serializer.errors})    
#             except:
#                 return Response({"Status":False, "Message":"Record not found !!!"})
#         else:
#             return Response({"Status":False, "Message":"Admin not found !!!"})  
        
#     def delete(self, request):
#         admin = get_object(request)
#         request.data["user_id"] = admin
#         get_admin = User.objects.get(id = admin.id)
#         if get_admin:
#             record_id = request.GET.get("transaction_id")
#             try:
#                 get_record = Transaction.objects.get(transaction_id = record_id)
#                 get_record.delete()
#                 return Response({"Status":True, "Message":"Record deleted successfully !!!"})
#             except:
#                 return Response({"Status":False, "Message":"Record not found !!!"})

          


        
