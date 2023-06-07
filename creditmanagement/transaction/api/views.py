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
            else:
                all_records_objs = Transaction.objects.filter(admin = get_admin, payment_request__payment_status = True)
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
                if get_request_obj.payment_status == False:
                    if data["payment_type"] != "":
                        if data["payment_type"] == "Full payment":
                            if data["paid_amount"] != "" and data["paid_amount"] >= get_request_obj.due_amount:
                                if data["due_paid_through"] != "": 
                                    data["card"] = get_request_obj.card.card_id
                                    data["user"] = get_request_obj.card.user_id.id
                                    data["payment_request"] = get_request_obj.request_id
                                    data["admin"] = get_admin.id
                                    get_request_obj.payment_status = data["payment_status"]
                                    get_request_obj.save()
                                    serializer = UserCardDepositPaymentSerializer(data=data)
                                    if serializer.is_valid():
                                        serializer.save()
                                        get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                        get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100 
                                        get_transaction_record.total_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100 + float(get_transaction_record.deposit_charges) + float(get_transaction_record.paid_amount)
                                        get_transaction_record.save()
                                        return onSuccess("Full Payment record added successfully !!!", serializer.data)
                                    else:
                                        return badRequest("Something went wrong !!!")
                                else:
                                    return badRequest("Please enter due paid through !!!")
                            else:
                                return badRequest("Please enter valid payment amount !!!")
                        else:
                            due_amount = get_request_obj.due_amount
                            get_transcation_records = Transaction.objects.filter(payment_request__request_id = data["request_id"])
                            serializer = AllTransactionRecordSerializer(get_transcation_records, many = True)
                            if len(get_transcation_records) > 0:
                                paid_sum = float(0)
                                for i in serializer.data:
                                    paid_sum += float(i["paid_amount"])
                                all_paid_sum = float(paid_sum) + float(data["paid_amount"])
                                # if float(all_paid_sum) <= float(due_amount):
                                #     return badRequest("Sum amount is not matching !!!")
                                if float(all_paid_sum) >= float(due_amount):
                                    data["card"] = get_request_obj.card.card_id
                                    data["user"] = get_request_obj.card.user_id.id
                                    data["payment_request"] = get_request_obj.request_id
                                    data["admin"] = get_admin.id
                                    get_request_obj.payment_status = data["payment_status"]
                                    get_request_obj.save()
                                    serializer = UserCardDepositPaymentSerializer(data=data)
                                    if serializer.is_valid():
                                        serializer.save()
                                        get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                        get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100 
                                        get_transaction_record.total_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100 + float(get_transaction_record.deposit_charges) + float(get_transaction_record.paid_amount)
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
                                        serializer = UserCardDepositPaymentSerializer(data=data)
                                        if serializer.is_valid():
                                            serializer.save()
                                            get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                            get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100 
                                            get_transaction_record.total_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100 + float(get_transaction_record.deposit_charges) + float(get_transaction_record.paid_amount)
                                            get_transaction_record.save()
                                            return onSuccess("Partial payment record added successfully", serializer.data)
                                        else:
                                            return badRequest(serializer.errors)                            
                                    else:
                                        return badRequest("You can not enter more than due amount !!!")
                            else:
                                if float(data['paid_amount']) < float(due_amount):
                                    data["card"] = get_request_obj.card.card_id
                                    data["user"] = get_request_obj.card.user_id.id
                                    data["payment_request"] = get_request_obj.request_id
                                    data["admin"] = get_admin.id
                                    serializer = UserCardDepositPaymentSerializer(data=data)
                                    if serializer.is_valid():
                                        serializer.save()
                                        get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                        get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100 
                                        get_transaction_record.total_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100 + float(get_transaction_record.deposit_charges) + float(get_transaction_record.paid_amount)
                                        get_transaction_record.save()
                                        return onSuccess("Partial payment record added successfully", serializer.data)
                                    else:
                                        return badRequest(serializer.errors)                            
                                else:
                                    return badRequest("You can not enter more than due amount !!!")
                    else:
                        return badRequest("Please select payment type !!!")
                else:
                    return badRequest("Payment already done !!!")    
                
            elif get_request_obj.payment_method == "Cycle":
                if get_request_obj.payment_status == False:
                    if get_request_obj.payment_method == "Cycle" and get_request_obj.cycle_deposit_status != True: 
                        print("if") 
                        if data["payment_type"] != "":
                            if data["payment_type"] == "Full payment":
                                if data["paid_amount"] != "" and data["paid_amount"] >= get_request_obj.due_amount:
                                    if data["due_paid_through"] != "": 
                                        data["card"] = get_request_obj.card.card_id
                                        data["user"] = get_request_obj.card.user_id.id
                                        data["payment_request"] = get_request_obj.request_id
                                        data["admin"] = get_admin.id
                                        # data["payment_method_flag"] = data
                                        get_request_obj.cycle_deposit_status = data["cycle_deposit_status"]
                                        get_request_obj.save()
                                        serializer = UserCardCycleandWithdrawPaymentSerializer(data=data)
                                        if serializer.is_valid():
                                            serializer.save()
                                            get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                            get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100
                                            get_transaction_record.total_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) + float(get_transaction_record.deposit_charges) /100 + float(get_transaction_record.paid_amount)
                                            get_transaction_record.save()
                                            return onSuccess("Full Payment record added successfully !!!", serializer.data)
                                    else:
                                        return badRequest("Please enter due paid through !!!")
                                else:
                                    return badRequest("Please enter valid payment amount !!!")
                            else:
                                due_amount = get_request_obj.due_amount
                                get_transcation_records = Transaction.objects.filter(payment_request__request_id = data["request_id"])
                                serializer = AllTransactionRecordSerializer(get_transcation_records, many = True)
                                if len(get_transcation_records) > 0:
                                    paid_sum = float(0)
                                    for i in serializer.data:
                                        paid_sum += float(i["paid_amount"])
                                    all_paid_sum = float(paid_sum) + float(data["paid_amount"])
                                    # if float(all_paid_sum) > float(due_amount):
                                    #     return badRequest("Sum amount is not matching !!!")
                                    if float(all_paid_sum) >= float(due_amount):
                                        data["card"] = get_request_obj.card.card_id
                                        data["user"] = get_request_obj.card.user_id.id
                                        data["payment_request"] = get_request_obj.request_id
                                        data["admin"] = get_admin.id
                                        get_request_obj.cycle_deposit_status = data["cycle_deposit_status"]
                                        get_request_obj.save()
                                        serializer = UserCardCycleandWithdrawPaymentSerializer(data=data)
                                        if serializer.is_valid():
                                            serializer.save()
                                            get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                            get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100
                                            get_transaction_record.total_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100 + float(get_transaction_record.deposit_charges) + float(get_transaction_record.paid_amount)
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
                                            serializer = UserCardCycleandWithdrawPaymentSerializer(data=data)
                                            if serializer.is_valid():
                                                serializer.save()
                                                get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                                get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100
                                                get_transaction_record.total_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100 + float(get_transaction_record.deposit_charges) + float(get_transaction_record.paid_amount)
                                                get_transaction_record.save()
                                                return onSuccess("Partial payment record added successfully", serializer.data)
                                            else:
                                                return badRequest(serializer.errors)                            
                                        else:
                                            return badRequest("You can not enter more than due amount !!!")
                                else:
                                    if float(data['paid_amount']) < float(due_amount):
                                        data["card"] = get_request_obj.card.card_id
                                        data["user"] = get_request_obj.card.user_id.id
                                        data["payment_request"] = get_request_obj.request_id
                                        data["admin"] = get_admin.id
                                        serializer = UserCardCycleandWithdrawPaymentSerializer(data=data)
                                        if serializer.is_valid():
                                            serializer.save()
                                            get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                            get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100
                                            get_transaction_record.total_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100 + float(get_transaction_record.deposit_charges) + float(get_transaction_record.paid_amount)
                                            get_transaction_record.save()
                                            return onSuccess("Partial payment record added successfully", serializer.data)
                                        else:
                                            return badRequest(serializer.errors)                            
                                    else:
                                        return badRequest("You can not enter more than due amount !!!")
                        else:
                            return badRequest("Please select payment type !!!")    
                    else:
                        print("else")
                        if data["payment_type"] != "":
                            if data["payment_type"] == "Full payment":
                                if data["paid_amount"] != "" and data["paid_amount"] >= get_request_obj.due_amount:
                                    if data["due_paid_through"] != "": 
                                        data["card"] = get_request_obj.card.card_id
                                        data["user"] = get_request_obj.card.user_id.id
                                        data["payment_request"] = get_request_obj.request_id
                                        data["admin"] = get_admin.id
                                        get_request_obj.cycle_withdraw_status = data["cycle_withdraw_status"]
                                        get_request_obj.payment_status = data["payment_status"]
                                        get_request_obj.save()
                                        serializer = UserCardCycleandWithdrawPaymentSerializer(data=data)
                                        if serializer.is_valid():
                                            serializer.save()
                                            get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                            get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100
                                            get_transaction_record.withdraw_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.withdraw_charges) /100
                                            get_transaction_record.total_amount =  float(get_transaction_record.profit) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.withdraw_charges) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.paid_amount)
                                            get_transaction_record.save()
                                            return onSuccess("Full Payment record added successfully !!!", serializer.data)
                                    else:
                                        return badRequest("Please enter due paid through !!!")
                                else:
                                    return badRequest("Please enter valid payment amount !!!")
                            else:
                                due_amount = get_request_obj.due_amount
                                get_transcation_records = Transaction.objects.filter(payment_request__request_id = data["request_id"])
                                serializer = AllTransactionRecordSerializer(get_transcation_records, many = True)
                                if len(get_transcation_records) > 0:
                                    paid_sum = float(0)
                                    for i in serializer.data:
                                        paid_sum += float(i["paid_amount"])
                                    all_paid_sum = float(paid_sum) + float(data["paid_amount"])
                                    # if float(all_paid_sum) > float(due_amount):
                                    #     return badRequest("Sum amount is not matching !!!")
                                    if float(all_paid_sum) >= float(due_amount):
                                        data["card"] = get_request_obj.card.card_id
                                        data["user"] = get_request_obj.card.user_id.id
                                        data["payment_request"] = get_request_obj.request_id
                                        data["admin"] = get_admin.id
                                        get_request_obj.cycle_withdraw_status = data["cycle_withdraw_status"]
                                        get_request_obj.payment_status = data["payment_status"]
                                        get_request_obj.save()
                                        serializer = UserCardCycleandWithdrawPaymentSerializer(data=data)
                                        if serializer.is_valid():
                                            serializer.save()
                                            get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                            get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100
                                            get_transaction_record.withdraw_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.withdraw_charges) /100
                                            get_transaction_record.total_amount =  float(get_transaction_record.profit) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.withdraw_charges) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.paid_amount)
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
                                            serializer = UserCardCycleandWithdrawPaymentSerializer(data=data)
                                            if serializer.is_valid():
                                                serializer.save()
                                                get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                                get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100
                                                get_transaction_record.withdraw_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.withdraw_charges) /100
                                                get_transaction_record.total_amount =  float(get_transaction_record.profit) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.withdraw_charges) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.paid_amount)
                                                get_transaction_record.save()
                                                return onSuccess("Partial payment record added successfully", serializer.data)
                                            else:
                                                return badRequest(serializer.errors)                            
                                        else:
                                            return badRequest("You can not enter more than due amount !!!")
                                else:
                                    if float(data['paid_amount']) < float(due_amount):
                                        data["card"] = get_request_obj.card.card_id
                                        data["user"] = get_request_obj.card.user_id.id
                                        data["payment_request"] = get_request_obj.request_id
                                        data["admin"] = get_admin.id
                                        serializer = UserCardCycleandWithdrawPaymentSerializer(data=data)
                                        if serializer.is_valid():
                                            serializer.save()
                                            get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                            get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100
                                            get_transaction_record.withdraw_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.withdraw_charges) /100
                                            get_transaction_record.total_amount =  float(get_transaction_record.profit) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.withdraw_charges) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.paid_amount)
                                            get_transaction_record.save()
                                            return onSuccess("Partial payment record added successfully", serializer.data)
                                        else:
                                            return badRequest(serializer.errors)                            
                                    else:
                                        return badRequest("You can not enter more than due amount !!!") 
                        else:
                            return badRequest("Please select payment type !!!") 
                else:
                    return badRequest("Payment already done !!!")
                        
            elif get_request_obj.payment_method == "Withdraw":
                if get_request_obj.payment_status == False:
                    if data["payment_type"] != "":
                        if data["payment_type"] == "Full payment":
                            if data["paid_amount"] != "" and data["paid_amount"] >= get_request_obj.due_amount:
                                if data["due_paid_through"] != "": 
                                    data["card"] = get_request_obj.card.card_id
                                    data["user"] = get_request_obj.card.user_id.id
                                    data["payment_request"] = get_request_obj.request_id
                                    data["admin"] = get_admin.id
                                    get_request_obj.payment_status = data["payment_status"]
                                    get_request_obj.save()
                                    serializer = UserCardCycleandWithdrawPaymentSerializer(data=data)
                                    if serializer.is_valid():
                                        serializer.save()
                                        get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                        get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100
                                        get_transaction_record.withdraw_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.withdraw_charges) /100
                                        get_transaction_record.total_amount =  float(get_transaction_record.profit) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.withdraw_charges) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.paid_amount)
                                        get_transaction_record.save()
                                        return onSuccess("Full Payment record added successfully !!!", serializer.data)
                                else:
                                    return badRequest("Please enter due paid through !!!")
                            else:
                                return badRequest("Please enter valid payment amount !!!")
                        else:
                            due_amount = get_request_obj.due_amount
                            get_transcation_records = Transaction.objects.filter(payment_request__request_id = data["request_id"])
                            serializer = AllTransactionRecordSerializer(get_transcation_records, many = True)
                            if len(get_transcation_records) > 0:
                                paid_sum = float(0)
                                for i in serializer.data:
                                    paid_sum += float(i["paid_amount"])
                                all_paid_sum = float(paid_sum) + float(data["paid_amount"])
                                # if float(all_paid_sum) > float(due_amount):
                                #     return badRequest("Sum amount is not matching !!!")
                                if float(all_paid_sum) >= float(due_amount):
                                    data["card"] = get_request_obj.card.card_id
                                    data["user"] = get_request_obj.card.user_id.id
                                    data["payment_request"] = get_request_obj.request_id
                                    data["admin"] = get_admin.id
                                    get_request_obj.payment_status = data["payment_status"]
                                    get_request_obj.save()
                                    serializer = UserCardCycleandWithdrawPaymentSerializer(data=data)
                                    if serializer.is_valid():
                                        serializer.save()
                                        get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                        get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100
                                        get_transaction_record.withdraw_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.withdraw_charges) /100
                                        get_transaction_record.total_amount =  float(get_transaction_record.profit) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.withdraw_charges) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.paid_amount)
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
                                        serializer = UserCardCycleandWithdrawPaymentSerializer(data=data)
                                        if serializer.is_valid():
                                            serializer.save()
                                            get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                            get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100
                                            get_transaction_record.withdraw_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.withdraw_charges) /100
                                            get_transaction_record.total_amount =  float(get_transaction_record.profit) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.withdraw_charges) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.paid_amount)
                                            get_transaction_record.save()
                                            return onSuccess("Partial payment record added successfully", serializer.data)
                                        else:
                                            return badRequest(serializer.errors)                            
                                    else:
                                        return badRequest("You can not enter more than due amount !!!")
                            else:
                                if float(data['paid_amount']) < float(due_amount):
                                    data["card"] = get_request_obj.card.card_id
                                    data["user"] = get_request_obj.card.user_id.id
                                    data["payment_request"] = get_request_obj.request_id
                                    data["admin"] = get_admin.id
                                    serializer = UserCardCycleandWithdrawPaymentSerializer(data=data)
                                    if serializer.is_valid():
                                        serializer.save()
                                        get_transaction_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                                        get_transaction_record.profit_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.profit) /100
                                        get_transaction_record.withdraw_amount = float(get_transaction_record.paid_amount) * float(get_transaction_record.withdraw_charges) /100
                                        get_transaction_record.total_amount =  float(get_transaction_record.profit) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.withdraw_charges) * float(get_transaction_record.paid_amount) /100 + float(get_transaction_record.paid_amount)                                       
                                        get_transaction_record.save()
                                        return onSuccess("Partial payment record added successfully", serializer.data)
                                    else:
                                        return badRequest(serializer.errors)                            
                                else:
                                    return badRequest("You can not enter more than due amount !!!") 
                    else:
                        return badRequest("Please select payment type !!!")
                else:
                    return badRequest("Payment already done !!!")
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
            request_id = request.GET.get("request_id")

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
                
            if request_id != None:
                try:
                    record_obj = Payment_Request.objects.get(request_id = request_id, admin = get_admin)
                except:
                    return badRequest("No Record with request id !!!")
                serializer = PaidUnpaidWithdrawSerializer(record_obj)
                return onSuccess("Record with request id !!!", serializer.data)

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

from django.db.models import Q

class DueProfitUnpaidProfitView(APIView):
    def get(self, request):
        token = get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin = True)
            except:
                return badRequest("Admin not found !!!")
            # start_date = request.GET.get("start_date")
            # end_date = request.GET.get("end_date")
            month = request.GET.get("month")
            payment_status = request.GET.get("payment_status")
            payment_received = request.GET.get("payment_received")
            # payment_method = request.GET.get("payment_method")

            if month != None:
                record_objs = Transaction.objects.filter(due_paid_at__month = month, admin = get_admin)
                if record_objs:
                    serializer = ProfitUnpaidProfitDetailsSerializer(record_objs, many = True)
                    return onSuccess("Records with given month !!!", serializer.data)
                else:
                    serializer = ProfitUnpaidProfitDetailsSerializer(record_objs, many = True)
                    return onSuccess("No Records with given month !!!", serializer.data)
        
            elif payment_status != None:
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

  
#--------------------------------- PDF CONVERT ----------------------------#

# from django.shortcuts import render
# from transaction.api.helpers import *

# class Generate_pdf(APIView):
#     def get(self, request, *args, **kwargs):
#         token = get_object(request)
#         if token:
#             try:
#                 get_admin = User.objects.get(id = token["user_id"], is_admin = True)
#             except:
#                 return badRequest("Admin not found !!!")
#             request_id = request.GET.get("request_id")
            
#             if request_id != None or 0:
#                 record_objs = Transaction.objects.filter(payment_request__request_id = request_id, admin = get_admin)
#                 serializer = AllTransactionRecordSerializer(record_objs, many = True)
#                 params = {
#                     'records' : serializer.data
#                 }
#                 file_name = render_to_pdf('pdf_convert/payment_summary.html', params)
                
#                 print("file name", file_name)   
#                 return onSuccess("Here is your pdf file", f'/static/{file_name}.pdf')
#             else:
#                 return badRequest("please enter a valid request id !!!")
#         else:
#             return unauthorisedRequest()
        



from django.http import HttpResponse
from django.template.loader import get_template
from transaction.api.helpers import *
from datetime import date

class Generate_pdf(APIView):
    def get(self, request, *args, **kwargs):
        token = get_object(request)
        if token:
            try:
                get_admin = User.objects.get(id = token["user_id"], is_admin = True)
            except:
                return badRequest("Admin not found !!!")
            request_id = request.GET.get("request_id")
            try:
                get_request = Payment_Request.objects.get(request_id = request_id)
            except:
                return badRequest("No request found for this request id !!!")
            try:
                record_objs = Transaction.objects.filter(payment_request__request_id = request_id, admin = get_admin)
            except:
                return badRequest("No records found with given request id !!!")
            serializer = AllTransactionRecordSerializer(record_objs, many = True)
            # print("serializer", serializer.data)
            paid_date = []
            tran_id = []
            charges_sum = []
            total_charge = 0
            total_payable_amount = 0
            deposit_amount = 0
            for i in range(len(serializer.data)):
                due_paid_at = serializer.data[i]["due_paid_at"]
                transaction_id = serializer.data[i]["transaction_id"]
                charge_sum = float(serializer.data[i]["deposit_charges"]) + float(serializer.data[i]["withdraw_amount"]) + float(serializer.data[i]["profit_amount"])
                stripped_date = due_paid_at[0:10]
                stripped_tran_id = transaction_id[-4:]
                paid_date.append(stripped_date)
                tran_id.append(stripped_tran_id)
                charges_sum.append(charge_sum)
                serializer.data[i]["due_paid_at"] = stripped_date
                serializer.data[i]["transaction_id"] = stripped_tran_id
                serializer.data[i]["charge_sum"] = charge_sum
                total_charge = charge_sum + total_charge
                if serializer.data[i]["payment_method_flag"] == "Cycle Deposit":
                    deposit_amount = serializer.data[i]["paid_amount"]  + deposit_amount
            total_payable_amount = total_payable_amount + deposit_amount + total_charge
            today = date.today()
            context = {
                'records' : serializer.data,
                'admin_name' : get_admin.first_name + " " + get_admin.last_name,
                'admin_email' : get_admin.email,
                'admin_mobile' : get_admin.phone_no,
                'today_date' : today.strftime("%B %d, %Y"),
                'user_name' : get_request.user.first_name + " " + get_request.user.last_name,
                'user_email' : get_request.user.email,
                'user_mobile' : get_request.user.phone_no,
                'payment_method': get_request.payment_method,
                'total_charge': total_charge,
                'total_payable_amount': total_payable_amount


            }
            pdf = render_to_pdf("pdf_convert/payment_summary.html", context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                # filename = "Invoice_%s.pdf" %("example")
                # content = "inline; filename='%s'" %(filename)
                # download = request.GET.get("download")
                # if download:
                #     content = "attachment; filename='%s'" %(filename)
                # response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
        else:
            return unauthorisedRequest()
