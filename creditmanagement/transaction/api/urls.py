from django.urls import path
from transaction.api.views import *

urlpatterns = [
    
    #------------------ GET ALL RECORDS (ADMIN ACCESS) -----------------#
    path ('all-payment-record-list', PaymentRecords.as_view(), name="GetAllPaymentRecords"),

    #------------ ADD USERS PAYMENT RECORD (ADMIN ACCESS) --------------#
    path ('add-payment-record', UserCardPayemtRecord.as_view(), name="UserCardPayemtRecord"),

    #------------ UPDATE AND DELETE PAYMENT RECORD (ADMIN ACCESS) -------#
    path ('edit-payment-record', UpdateTransactionRecord.as_view(), name="UpdateDeleteTransactionRecord"),
    path ('delete-payment-record', UpdateTransactionRecord.as_view(), name="UpdateDeleteTransactionRecord"),


    #------------------------- DASHBOARD DATA VIEWS ---------------------#

    #------------------------- DATA WITH STATUS AND METHOD --------------#
    path ('paid-unpaid-withdraw', PaidUnpaidWithdrawView.as_view(), name="PaidUnpaidWithdrawView"),


    path ('profit-unpaidprofit-view', DueProfitUnpaidProfitView.as_view(), name="DueProfitUnpaidProfitView"),

    #--------------- PDF -----------------------#

    path ('pdf', Generate_pdf.as_view(), name="Generate_pdf"),




    # path("all-record", GetrecordList.as_view(), name="GetrecordList"),

    # ##### RECORDS CRUD #####

    # path("add-record", PaymentRecord.as_view(), name="PaymentRecord"),
    # path("edit-record", PaymentRecord.as_view(), name="PaymentRecord"),
    # path("delete-record", PaymentRecords.as_view(), name="PaymentRecord"),


]