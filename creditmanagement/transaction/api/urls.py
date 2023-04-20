from django.urls import path
from transaction.api.views import *

urlpatterns = [
    
    #------------------ GET ALL RECORDS (ADMIN ACCESS) -----------------#
    path ('all-payment-record-list', PaymentRecords.as_view(), name="GetAllPaymentRecords"),

    #------------ ADD USERS PAYMENT RECORD (ADMIN ACCESS) --------------#
    path ('add-payment-record', UserCardPayemtRecord.as_view(), name="UserCardPayemtRecord"),

    #------------ UPDATE AND DELETE PAYMENT RECORD (ADMIN ACCESS) -------#
    path ('edit-payment-record', UpdateDeleteTransactionRecord.as_view(), name="UpdateDeleteTransactionRecord"),
    path ('delete-payment-record', UpdateDeleteTransactionRecord.as_view(), name="UpdateDeleteTransactionRecord"),



    # path("all-record", GetrecordList.as_view(), name="GetrecordList"),

    # ##### RECORDS CRUD #####

    # path("add-record", PaymentRecord.as_view(), name="PaymentRecord"),
    # path("edit-record", PaymentRecord.as_view(), name="PaymentRecord"),
    # path("delete-record", PaymentRecord.as_view(), name="PaymentRecord"),


]