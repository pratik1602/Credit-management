from django.urls import path
from PaymentRequest.api.views import *

urlpatterns = [

    #--------------------- ADD PAYMENT REQUEST (ADMIN) ------------------#
    path ('add-payment-request-byadmin', AddPaymentRequestByAdmin.as_view(), name="AddPaymentRequestByAdmin"),
    
    #--------------------- ADD PAYMENT REQUEST (USER) ------------------#
    path ('add-payment-request-byuser', AddPaymentRequestByUser.as_view(), name="AddPaymentRequestByUser"), 


]