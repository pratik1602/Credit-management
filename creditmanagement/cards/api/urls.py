from django.urls import path
from cards.api.views import *

urlpatterns = [

    #--------------------- USER'S CARD LIST (ADMIN ACCESS) ------------------#
    path ('cards-list', GetCardList.as_view(), name="GetCardList"),


    #--------------------- USER'S CARD VIEWS -----------------------------#
    path ('card-view', UserCardAPIView.as_view(), name="UserCardAPIView"),
    path ('add-card', UserCardAPIView.as_view(), name="UserCardAPIView"),
    path ('edit-card', UserCardAPIView.as_view(), name="UserCardAPIView"),
    path ('delete-card', UserCardAPIView.as_view(), name="UserCardAPIView"),


    #-------------------- ADMIN CARDS VIEWS ----------------------------#
    path('view-admin-card', AdminCards.as_view(), name="AdminCards"),
    path('add-admin-card', AdminCards.as_view(), name="AdminCards"),
    path('edit-admin-card', AdminCards.as_view(), name="AdminCards"),
    path('delete-admin-card', AdminCards.as_view(), name="AdminCards"),


    #--------- CREATE AND UPDATE USER'S CARD (ADMIN ACCESS) ------------#
    path ('add-user-card', UserCard.as_view(), name="AddUserCard"),
    path ('edit-user-card', UserCard.as_view(), name="AddUserCard"),



]