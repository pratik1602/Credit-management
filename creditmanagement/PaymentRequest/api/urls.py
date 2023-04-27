from django.urls import path
from PaymentRequest.api.views import *

urlpatterns = [
    #--------------------- ALL PAYMENT REQUEST (ADMIN) ------------------#
    path ('payment-request-list', GetPaymentRequest.as_view(), name="GetPaymentRequest"), 

    #--------------------- ADD PAYMENT REQUEST (ADMIN) ------------------#
    path ('add-payment-request-byadmin', AddPaymentRequestByAdmin.as_view(), name="AddPaymentRequestByAdmin"),
    
    #--------------------- ADD PAYMENT REQUEST (USER) ------------------#
    path ('add-payment-request-byuser', AddPaymentRequestByUser.as_view(), name="AddPaymentRequestByUser"), 
    


]