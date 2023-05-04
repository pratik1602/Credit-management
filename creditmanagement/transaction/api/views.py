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
            except:
                return badRequest("Admin not found !!!")
            data = request.data
            try:
                get_request_obj = Payment_Request.objects.get(request_id = data["request_id"])
            except:
                return badRequest("No Request found !!!")
            
            if get_request_obj.payment_method == "Deposit":
                if data["payment_type"] != "":
                    if data["payment_type"] == "Full payment":
                        if data["paid_amount"] != "" and data["paid_amount"] == get_request_obj.due_amount:
                            if data["due_paid_through"] != "": 
                                data["card"] = get_request_obj.card.card_id
                                data["user"] = get_request_obj.card.user_id.id
                                data["payment_request"] = get_request_obj.request_id
                                data["admin"] = get_admin.id
                                get_request_obj.payment_status = data["payment_status"]
                                get_request_obj.save()
                                serializer = UserCardPaymentSerializer(data=data)
                                if serializer.is_valid():
                                    serializer.save()
                                    get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                    get_transaction_record.profit_amount = get_transaction_record.paid_amount * get_transaction_record.profit /100 + get_transaction_record.charges
                                    get_transaction_record.save()
                                    return onSuccess("Full Payment record added successfully !!!", serializer.data)
                            else:
                                return badRequest("Please enter due paid through !!!")
                        else:
                            return badRequest("Please enter full payment amount !!!")
                    else:
                        due_amount = get_request_obj.due_amount
                        get_transcation_records = Transaction.objects.filter(payment_request__request_id = data["request_id"])
                        serializer = AllTransactionRecordSerializer(get_transcation_records, many = True)
                        if len(get_transcation_records) > 0:
                            paid_sum = 0
                            for i in serializer.data:
                                paid_sum += int(i["paid_amount"]) 
                            all_paid_sum = paid_sum + data["paid_amount"]
                            if float(all_paid_sum) > float(due_amount):
                                return badRequest("Sum amount is not matching !!!")
                            if float(due_amount) == float(all_paid_sum):
                                get_request_obj.payment_status = data["payment_status"]
                                data["card"] = get_request_obj.card.card_id
                                data["user"] = get_request_obj.card.user_id.id
                                data["payment_request"] = get_request_obj.request_id
                                data["admin"] = get_admin.id
                                get_request_obj.save()
                                serializer = UserCardPaymentSerializer(data=data)
                                if serializer.is_valid():
                                    serializer.save()
                                    get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                    get_transaction_record.profit_amount = get_transaction_record.paid_amount * get_transaction_record.profit /100 + get_transaction_record.charges
                                    get_transaction_record.save()
                                    return onSuccess("Partial payment record added successfully", serializer.data)
                                else:
                                    return badRequest(serializer.errors)
                            else:
                                if float(data['paid_amount']) < float(due_amount):
                                    data["card"] = get_request_obj.card.card_id
                                    data["user"] = get_request_obj.card.user_id.id
                                    data["payment_request"] = get_request_obj.request_id
                                    data["admin"] = get_admin.id
                                    serializer = UserCardPaymentSerializer(data=data)
                                    if serializer.is_valid():
                                        serializer.save()
                                        get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                        get_transaction_record.profit_amount = get_transaction_record.paid_amount * get_transaction_record.profit /100 + get_transaction_record.charges
                                        get_transaction_record.save()
                                        return onSuccess("Partial payment record added successfully", serializer.data)
                                    else:
                                        badRequest(serializer.errors)                            
                                else:
                                    return badRequest("You can not enter more than due amount !!!")
                        else:
                            if float(data['paid_amount']) < float(due_amount):
                                data["card"] = get_request_obj.card.card_id
                                data["user"] = get_request_obj.card.user_id.id
                                data["payment_request"] = get_request_obj.request_id
                                data["admin"] = get_admin.id
                                serializer = UserCardPaymentSerializer(data=data)
                                if serializer.is_valid():
                                    serializer.save()
                                    get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                    get_transaction_record.profit_amount = get_transaction_record.paid_amount * get_transaction_record.profit /100 + get_transaction_record.charges
                                    get_transaction_record.save()
                                    return onSuccess("Partial payment record added successfully", serializer.data)
                                else:
                                    badRequest(serializer.errors)                            
                            else:
                                return badRequest("You can not enter more than due amount !!!")
            else:
                return badRequest("Please select payment type !!!")
        else:
            return unauthorisedRequest()

class UpdateTransactionRecord(APIView):
    def patch(self, request):
        token = get_object(request)
        if token:
            try:
                User.objects.get(id = token["user_id"], is_admin = True)
            except:
                return badRequest("Admin not found !!!")
            data = request.data
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


#--------------------------////// DASHBOARD APIS //////------------------------#

#-------------------------- PAID, UNPAID, WITHDRAW ----------------------------#

class PaidUnpaidWithdrawView(APIView):
    def get(self, request):
        token = get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin = True)
            except:
                return badRequest("Admin not found !!!")
            payment_method = request.GET.get("payment_method")
            payment_status = request.GET.get("payment_status")

            if payment_status != None:
                record_objs = Payment_Request.objects.filter(payment_status = payment_status, admin = get_admin)
                if record_objs:
                    serializer = PaidUnpaidWithdrawSerializer(record_objs, many = True)
                    return onSuccess("Records with payment status !!!", serializer.data)
                else:
                    serializer = PaidUnpaidWithdrawSerializer(record_objs, many = True)
                    return onSuccess("No Records with payment status !!!", serializer.data)
            if payment_method != None:
                record_objs = Payment_Request.objects.filter(payment_method = payment_method, admin = get_admin)
                if record_objs:
                    serializer = PaidUnpaidWithdrawSerializer(record_objs, many = True)
                    return onSuccess("Records with payment method !!!", serializer.data)
                else:
                    serializer = PaidUnpaidWithdrawSerializer(record_objs, many = True)
                    return onSuccess("No Records with payment method !!!", serializer.data)
            else:
                all_records_objs = Payment_Request.objects.filter(admin = get_admin)
                if all_records_objs:
                    serializer = PaidUnpaidWithdrawSerializer(all_records_objs, many=True)
                    return onSuccess("Records List !!!",  serializer.data)
                else:
                    serializer = PaidUnpaidWithdrawSerializer(all_records_objs, many=True)
                    return onSuccess("Records List !!!",  serializer.data)        
        else:
            return unauthorisedRequest()


#-------------------------- PROFIT, UNPAID PROFIT, DUE AMOUNT, UNPAID AMOUNT VIEWS ----------------------------#

class DueProfitUnpaidProfitView(APIView):
    def get(self, request):
        token = get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin = True)
            except:
                return badRequest("Admin not found !!!")
            payment_status = request.GET.get("payment_status")
            payment_received = request.GET.get("payment_received")
            # payment_method = request.GET.get("payment_method")
                
            if payment_status != None:
                record_objs = Transaction.objects.filter(payment_request__payment_status = payment_status, admin = get_admin)
                if record_objs:
                    serializer = ProfitUnpaidProfitDetailsSerializer(record_objs, many = True)
                    return onSuccess("Records with payment status !!!", serializer.data)
                else:
                    serializer = ProfitUnpaidProfitDetailsSerializer(record_objs, many = True)
                    return onSuccess("No Records with payment status !!!", serializer.data)
                
            elif payment_received != None:
                record_objs = Transaction.objects.filter(payment_received = payment_received, admin = get_admin)
                if record_objs:
                    serializer = ProfitUnpaidProfitDetailsSerializer(record_objs, many = True)
                    return onSuccess("Records with User's payment received status !!!", serializer.data)
                else:
                    serializer = ProfitUnpaidProfitDetailsSerializer(record_objs, many = True)
                    return onSuccess("No Records with User's payment received status !!!", serializer.data)
            
            # elif payment_method != None:
            #     record_objs = Transaction.objects.filter(payment_request__payment_method = payment_method)
            #     if record_objs:
            #         serializer = ProfitUnpaidProfitDetailsSerializer(record_objs, many = True)
            #         return onSuccess("Records with payment method !!!", serializer.data)
            #     else:
            #         serializer = ProfitUnpaidProfitDetailsSerializer(record_objs, many = True)
            #         return onSuccess("No Records with payment method !!!", serializer.data)
            else:
                all_records_objs = Transaction.objects.filter(admin = get_admin)
                if all_records_objs:
                    serializer = ProfitUnpaidProfitDetailsSerializer(all_records_objs, many=True)
                    return onSuccess("Records List !!!",  serializer.data)
                else:
                    serializer = ProfitUnpaidProfitDetailsSerializer(all_records_objs, many=True)
                    return onSuccess("Records List !!!",  serializer.data)        
        else:
            return unauthorisedRequest()


#----------------------------- TOTAL CARDS AND PROFIT AMOUNT ----------------------------#

# class TotalCardsandProfitAmountView(APIView):

#     def get(self, request):
#         token = get_object(request)
#         if token:
#             try:
#                 get_admin = User.objects.get(id = token["user_id"], is_admin = True)
#             except:
#                 return badRequest("Admin not found !!!")
            
#         else:
#             return unauthorisedRequest() 
        
