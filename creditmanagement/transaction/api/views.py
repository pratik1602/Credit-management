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


#--------------- GET TRANSACTION RECORD LIST  ----------------#

class GetrecordList(APIView):
    def get(self, request):
        token = get_object(request)
        if token:
            get_admin = User.objects.get(id = token["user_id"])
            if get_admin and get_admin.is_admin:
                record_id = request.GET.get("transaction_id")
                if record_id != None or 0:
                    try:
                        record_obj = Transaction.objects.get(transaction_id=record_id)
                        serializer = RecordSerializer(record_obj)
                        return onSuccess("Record !!!", serializer.data)
                        # return Response({"Status": True, "Message": "Record !!!", "Data": serializer.data})
                    except:
                        return badRequest("No Record found !!!")
                        # return Response({"Status": False, "Message": "No Record found !!!"})
                else:
                    record_objs = Transaction.objects.all()
                    if record_objs:
                        serializer = RecordSerializer(record_objs, many=True)
                        return onSuccess("Records List", serializer.data)
                        # return Response({"Status": True, "Message": "Records List", "Data": serializer.data})
                    else:
                        serializer = RecordSerializer(record_objs, many=True)
                        return onSuccess("No Records found !!!", serializer.data)  
                        # return Response({"Status": False, "Message": "No Records found !!!", "Data": serializer.data})  
            else:
                return badRequest("No Admin Found !!!")
                # return Response({"Status": False, "Message":"No Admin Found !!!"})
        else:
            return unauthorisedRequest()

             
#------------------ TRANSACTIONS RECORD CRUD ---------------------------#

class PaymentRecord(APIView):
    permission_classes = [IsAuthenticated&IsAdminUser]

    def post(self, request):
        admin = get_object(request)
        request.data["user_id"] = admin
        get_admin = User.objects.get(id = admin.id)
        if get_admin:
            data = request.data
            try:
                get_card_id = data["card"]
                get_card = Card.objects.get(card_id = get_card_id)
                print("get_card", get_card)
            except:
                return Response({"Status":False, "Message":"Card not found !!!"})
            serializer = RecordSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                get_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                Total_profit_amount =  get_record.amount_paid * get_record.commission/100 
                get_record.profit_amount = "%.2f" % float(Total_profit_amount)
                get_record.card = get_card
                get_record.admin = get_admin
                get_record.save()
                return Response({"Status":True, "Message":"Record Added Successfully !!!"})
            else:
                return Response({"Status":False, "Data":serializer.errors})
        else:
            return Response({"Status":False, "Message":"Admin not found !!!"})
        
    def put(self, request):
        admin = get_object(request)
        request.data["user_id"] = admin
        get_admin = User.objects.get(id = admin.id)
        if get_admin:
            try:
                data = request.data
                get_record = Transaction.objects.get(transaction_id = data["transaction_id"])
                serializer = RecordSerializer(get_record, data=data)   
                if serializer.is_valid(): 
                    serializer.save()
                    get_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                    get_record.profit_amount = get_record.amount_paid * get_record.commission/100
                    get_record.save()
                    return Response({"Status":True, "Message":"Record Updated successfully !!!"})
                else:
                    return Response({"Status":False, "Data":serializer.errors})    
            except:
                return Response({"Status":False, "Message":"Record not found !!!"})
        else:
            return Response({"Status":False, "Message":"Admin not found !!!"})  
        
    def delete(self, request):
        admin = get_object(request)
        request.data["user_id"] = admin
        get_admin = User.objects.get(id = admin.id)
        if get_admin:
            record_id = request.GET.get("transaction_id")
            try:
                get_record = Transaction.objects.get(transaction_id = record_id)
                get_record.delete()
                return Response({"Status":True, "Message":"Record deleted successfully !!!"})
            except:
                return Response({"Status":False, "Message":"Record not found !!!"})

          


        
