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
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin = True)
            except:
                return badRequest("Admin not found !!!")
            transaction_id = request.GET.get("transaction_id")
            user_id = request.GET.get("user_id")
            card_id = request.GET.get("card_id")
            request_id = request.GET.get("request_id")
            payment_status = request.GET.get("payment_status")

            if transaction_id != None or 0:
                try:
                    record_obj = Transaction.objects.get(transaction_id = transaction_id, admin = get_admin)
                    serializer = AllTransactionRecordSerializer(record_obj)
                    return onSuccess("Transaction Record !!!", serializer.data)
                except:
                    return badRequest("No records found !!!")
                
            elif user_id != None or 0:
                try:
                    get_user = User.objects.get(id = user_id)
                except:
                    return badRequest("User not found !!!")
                record_objs = Transaction.objects.filter(user = get_user, admin = get_admin)
                if record_objs.exists():
                    serializer = AllTransactionRecordSerializer(record_objs, many = True)
                    return onSuccess("User's all transactions !!!", serializer.data)
                else:
                    serializer = AllTransactionRecordSerializer(record_objs, many = True)
                    return onSuccess("No Transactions found for user !!!", serializer.data)
                
            elif card_id != None or 0:
                record_objs = Transaction.objects.filter(card__card_id = card_id, admin = get_admin)
                if record_objs:
                    serializer = AllTransactionRecordSerializer(record_objs, many = True)
                    return onSuccess("Records with Card id !!!", serializer.data)
                else:
                    serializer = AllTransactionRecordSerializer(record_objs, many = True)
                    return onSuccess("No Records found with given Card id !!!", serializer.data)
            
            elif request_id != None or 0:
                record_objs = Transaction.objects.filter(payment_request__request_id = request_id, admin = get_admin)
                if record_objs:
                    serializer = AllTransactionRecordSerializer(record_objs, many = True)
                    return onSuccess("Records with request id !!!", serializer.data)
                else:
                    serializer = AllTransactionRecordSerializer(record_objs, many = True)
                    return onSuccess("No Records found with given request id !!!", serializer.data)
                
            elif payment_status != None:
                record_objs = Transaction.objects.filter(payment_request__payment_status = payment_status, admin = get_admin)
                if record_objs:
                    serializer = AllTransactionRecordSerializer(record_objs, many = True)
                    return onSuccess("Records with payment status !!!", serializer.data)
                else:
                    serializer = AllTransactionRecordSerializer(record_objs, many = True)
                    return onSuccess("No Records with payment status !!!", serializer.data)
            else:
                all_records_objs = Transaction.objects.filter(admin = get_admin)
                if all_records_objs:
                    serializer = AllTransactionRecordSerializer(all_records_objs, many=True)
                    return onSuccess("Records List !!!",  serializer.data)
                else:
                    serializer = AllTransactionRecordSerializer(all_records_objs, many=True)
                    return onSuccess("Records List !!!",  serializer.data)
        else:
            return unauthorisedRequest()

             
#------------------ TRANSACTIONS RECORD CRUD ---------------------------#

class UserCardPayemtRecord(APIView):
    def post(self, request):
        token = get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin = True)
                print("admin", get_admin)
            except:
                return badRequest("Admin not found !!!")
            data = request.data
            try:
                get_request_obj = Payment_Request.objects.get(request_id = data["request_id"])
                print("req", get_request_obj)
            except:
                return badRequest("No Request found !!!")
            if data["payment_type"] != "" and data["paid_amount"] != "" and data["due_paid_through"] != "": 
                data["card"] = get_request_obj.card.card_id
                data["user"] = get_request_obj.card.user_id.id
                data["payment_request"] = get_request_obj.request_id
                data["admin"] = get_admin.id
                get_request_obj.payment_status = data["payment_status"]
                get_request_obj.save()
                serializer = UserCardPaymentSerializer(data=data)
                
                if serializer.is_valid():
                    serializer.save()
                    # get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                    # get_transaction_record.payment_request.payment_status = data["payment_status"]
                    return onSuccess("Payment record added successfully !!!", serializer.data)

                else:
                    return badRequest(serializer.errors)  

                    # return badRequest("Something went wrong !!!")  
            else:
                return badRequest("Fields is missing !!!")
        else:
            return unauthorisedRequest()

# class UpdateDeleteTransactionRecord(APIView):
#     def patch(self, request):
#         token = get_object(request)
#         if token:
#             get_admin = User.objects.get(id = token["user_id"])
#             if get_admin and get_admin.is_admin:
#                 data = request.data
#                 if data["due_paid_through"] != "" and data["paid_amount"] != "" and data["due_paid_date"] != "" and data["due_paid_time"] != "":
#                     try:
#                         get_transaction = Transaction.objects.get(transaction_id = data["transaction_id"])
#                     except:
#                         return badRequest("No Record found !!!")
#                     serializer = EditTransactionRecordSerializer(get_transaction, data=data, partial = True)
#                     if serializer.is_valid():
#                         serializer.save()
#                         return onSuccess("Record Updated Successfully !!!", serializer.data)
#                     else:
#                         return badRequest("Something went wrong !!!")
#                 else:
#                     return badRequest("Fields is missing !!!")
#             else:
#                 return badRequest("Admin not found !!!")
#         else:
#             return unauthorisedRequest()
        
#     def delete(self, request):
#         token = get_object(request)
#         if token:
#             get_admin = User.objects.get(id = token['user_id'])
#             if get_admin and get_admin.is_admin:
#                 transaction_id = request.GET.get("transaction_id") 
#                 try:
#                     get_record = Transaction.objects.get(transaction_id = transaction_id)
#                     get_record.delete()
#                     return onSuccess("Record deleted successfully !!!", 1)
#                 except:
#                     return badRequest("Record not found !!!")
#             else:
#                 return badRequest("Admin not found !!!")
#         else:
#             return unauthorisedRequest()





        
