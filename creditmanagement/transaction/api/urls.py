from django.urls import path
from transaction.api.views import *

urlpatterns = [

    ##### GET ALL RECORDS #####

    path ('all-payment-record-list', PaymentRecords.as_view(), name="GetAllPaymentRecords"),

    # path("all-record", GetrecordList.as_view(), name="GetrecordList"),

    # ##### RECORDS CRUD #####

    # path("add-record", PaymentRecord.as_view(), name="PaymentRecord"),
    # path("edit-record", PaymentRecord.as_view(), name="PaymentRecord"),
    # path("delete-record", PaymentRecord.as_view(), name="PaymentRecord"),


]