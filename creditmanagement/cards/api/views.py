from rest_framework.response import Response
from usercredit.models import *
from cards.api.serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from core.decode import get_object
from datetime import datetime
from core.response import *
from django.db.models import Q

#-------------------- USER'S CARDS LIST (ADMIN ACCESS) ------------------------#

class GetCardList(APIView):

    def get(self, request):
        token = get_object(request)
        if token:
            get_admin = User.objects.get(id = token["user_id"])
            if get_admin and get_admin.is_admin:
                card_id = request.GET.get("card_id")
                user_id = request.GET.get("user_id")
                if card_id != None or 0:
                    try:
                        card_obj = Card.objects.get(user_id__under_by = get_admin, card_id=card_id)
                        serializer = AllCardSerializer(card_obj)
                        return onSuccess("Card !!!", serializer.data)
                    except:
                        return badRequest("No card found !!!")
                    
                elif user_id != None or 0:
                    try:
                        get_user = User.objects.get(id = user_id)
                        cards_objs = Card.objects.filter(user_id__under_by = get_admin, user_id = get_user)
                        if cards_objs:
                            serializer = AllCardSerializer(cards_objs, many=True)
                            return onSuccess("User's Card List !!!", serializer.data)
                        else:
                            serializer = AllCardSerializer(cards_objs, many=True)
                            return onSuccess("User's Card List !!!", serializer.data)
                    except:
                        return badRequest("No User found !!!")
                    
                else:
                    cards_objs = Card.objects.filter(user_id__under_by = get_admin)
                    if cards_objs:
                        serializer = AllCardSerializer(cards_objs, many=True)
                        return onSuccess("Cards List !!!",  serializer.data)
                    else:
                        serializer = AllCardSerializer(cards_objs, many=True)
                        return onSuccess("Cards List !!!",  serializer.data)
            else:
                return badRequest("No Admin Found !!!")
        else:
            return unauthorisedRequest()
        
  
#--------------- USER'S CREDIT CARDS LIST, CREATE ,UPDATE AND DELETE (USER) -------------#

class UserCardAPIView(APIView):
    def get(self, request):
        token = get_object(request) 
        if token:
            get_user = User.objects.get(id = token["user_id"])
            if get_user and get_user.is_verified:
                card_id = request.GET.get("card_id")
                if card_id != None or 0:
                    try:
                        card_obj = Card.objects.get(card_id=card_id, user_id=get_user)
                        serializer = UserCardSerializer(card_obj)
                        return onSuccess("Your Card !!!", serializer.data)
                    except:
                        return badRequest( "No card found !!!")
                else:
                    card_objs = Card.objects.filter(user_id=get_user)
                    if card_objs:
                        serializer = UserCardSerializer(card_objs, many=True)
                        return onSuccess("Your Cards !!!", serializer.data)
                    else:
                        serializer = UserCardSerializer(card_objs, many=True)
                        return onSuccess("Your Cards !!!", serializer.data)
            else:
                return badRequest("No User Found or not verified !!!")
        else:
            return unauthorisedRequest()

    def post(self, request): 
        token = get_object(request)
        if token:
            get_user = User.objects.get(id= token["user_id"])
            if get_user and get_user.is_verified:
                data = request.data
                if data["card_bank_name"] != "" and data["card_category"] != "" and data["card_number"] != "" and data["card_network"] != "" and data["card_holder_name"] != "" and data["card_photo"] != "" and data["card_exp_date"] != "" and  data["card_cvv"] != "" and data["due_date"] != "" and data["due_amount"] != "":
                    user_card_number = Card.objects.filter(card_number = data["card_number"])
                    if not user_card_number:
                        data["created_by"] = get_user.id
                        data["updated_by"] = get_user.id
                        data["due_amount"] = "%.2f" % float(data["due_amount"])
                        serializer = UserCardSerializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                            getCard = Card.objects.get(card_id=serializer.data["card_id"])
                            
                            getCard.profit_amount =  getCard.due_amount * getCard.commission/100
                            getCard.profit_amount = "%.2f" % float(getCard.profit_amount)
                            getCard.user_id = get_user
                            getCard.created_by = get_user
                            getCard.updated_by = get_user
                            getCard.save()
                            return onSuccess("Card Added Successfully", serializer.data)
                        else:
                            return badRequest("Something went wrong !!!")
                    else:
                        return badRequest("Invalid card number or already exists !!!")
                else:
                    return badRequest("Fields is missing !!!")
            else:
                return badRequest("User not found or not verified !!!")
        else:
            return unauthorisedRequest()

    def patch(self, request):
        token = get_object(request)
        if token:
            get_user = User.objects.get(id = token["user_id"])
            if get_user and get_user.is_verified:
                try:
                    data = request.data
                    get_card = Card.objects.get(card_id = data["card_id"])  
                    data["due_amount"] = "%.2f" % float(data["due_amount"])
                    serializer = UserCardSerializer(get_card ,data=data, partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        get_card.profit_amount =  get_card.due_amount * get_card.commission / 100
                        get_card.profit_amount = "%.2f" % float(get_card.profit_amount)
                        get_card.updated_by = get_user
                        get_card.modified_at = datetime.now()
                        get_card.save()
                        return onSuccess("Card updated Successfully !!!", serializer.data)
                    else:
                        return badRequest("Something went wrong !!!")

                except:
                    return badRequest("Card doesn't exixts !!!")
            else:
                return badRequest("User not found !!!")
        else:
            return unauthorisedRequest()

    def delete(self, request):
        token = get_object(request)
        if token:
            get_user = User.objects.get(id = token["user_id"])
            if get_user and get_user.is_verified:
                card_id = request.GET.get("card_id")
                try:
                    card_obj = Card.objects.get(card_id=card_id, user_id=get_user)
                    card_obj.delete()
                    return onSuccess("Card deleted successfully !!!", 1)
                except:
                    return badRequest("Card doesn't exists")
            else:
                return badRequest("No user found !!!")
        else:
            return unauthorisedRequest()


#--------------- ADMIN CARDS LIST, CREATE, UPDATE AND DELETE (ADMIN) -------------------#

class AdminCards(APIView):
    def get(self, request):
        token = get_object(request)
        if token:
            get_admin = User.objects.get(id = token["user_id"])
            if get_admin and get_admin.is_admin:
                card_id = request.GET.get("card_id")
                card_type = request.GET.get("card_type")
                if card_id != None or 0:
                    try:
                        card_obj = Card.objects.get(card_id=card_id, user_id=get_admin)
                        serializer = AdminAllcardSerializer(card_obj)
                        return onSuccess("Your Card !!!", serializer.data)
                    except:
                        return badRequest("No card found !!!")  
                else:
                    if card_type:
                        card_objs = Card.objects.filter(user_id=get_admin, card_type = card_type)
                    else:
                        card_objs = Card.objects.filter(user_id=get_admin)
 
                    serializer = AdminAllcardSerializer(card_objs, many=True)
                    return onSuccess("Your Cards !!!", serializer.data)  
            else:
                return badRequest("No Admin Found !!!")
        else:
            return unauthorisedRequest()

    def post(self, request):
        token = get_object(request)
        if token:
            get_admin = User.objects.get(id = token["user_id"])
            if get_admin and get_admin.is_admin:
                data = request.data
                if data["card_type"] == "Debit Card":
                    if data["card_bank_name"] != "" and data["card_number"] != "" and data["card_network"] != "" and data["card_holder_name"] != "" and data["card_photo"] != "" and data["card_exp_date"] != "" and  data["card_cvv"] != ""  and data["available_balance"] != "" and data["card_type"] != "":
                        user_card_number = Card.objects.filter(card_number = data["card_number"])
                        if not user_card_number:   
                            data["user_id"] = get_admin.id
                            data["available_balance"] = "%.2f" % float(data["available_balance"])
                            serializer = AdminDebitCardSerializer(data=data)
                            if serializer.is_valid():
                                serializer.save()
                                return onSuccess("Debit card added successfully !!!", serializer.data)
                            else:
                                return badRequest("Something went wrong !!!")
                        else:
                            return badRequest("Card with this card number already exists !!!")
                    else:
                        return badRequest("Fields is missing !!!")
                else:
                    if data["card_bank_name"] != "" and data["card_category"] != "" and data["card_number"] != "" and data["card_network"] != "" and data["card_holder_name"] != "" and data["card_photo"] != "" and data["card_exp_date"] != "" and  data["card_cvv"] != ""  and data["credit_amount"] != "" and data["card_type"] != "":
                        user_card_number = Card.objects.filter(card_number = data["card_number"])
                        if not user_card_number:   
                            data["user_id"] = get_admin.id
                            data["credit_amount"] = "%.2f" % float(data["credit_amount"])
                            serializer = AdminCreditCardSerializer(data=data)
                            if serializer.is_valid():
                                serializer.save()
                                return onSuccess("Credit card added successfully !!!", serializer.data)
                            else:
                                return badRequest("Something went wrong !!!")
                        else:
                            return badRequest("Card with this card number already exists !!!")
                    else:
                        return badRequest("Fields is missing !!!")
            else:
                return badRequest("Admin not found !!!")
        else:
            return unauthorisedRequest()
            
    def patch(self, request):
        token = get_object(request)
        if token:
            get_admin = User.objects.get(id = token["user_id"])
            if get_admin and get_admin.is_admin:
                if data["card_type"] == "Debit Card":
                    try:
                        data = request.data
                        get_card = Card.objects.get(card_id = data["card_id"])
                        data["available_balance"] = "%.2f" % float(data["available_balance"])
                        serializer = AdminAllcardSerializer(get_card ,data=data, partial = True)
                        if serializer.is_valid():
                            serializer.save()
                            return onSuccess("Card updated Successfully !!!", serializer.data)
                        else:
                            return badRequest("Something went wrong !!! ")
                    except:
                        return badRequest("Card doesn't exixts !!!")
                else:
                    try:
                        data = request.data
                        get_card = Card.objects.get(card_id = data["card_id"])
                        data["credit_amount"] = "%.2f" % float(data["credit_amount"])
                        serializer = AdminAllcardSerializer(get_card ,data=data, partial = True)
                        if serializer.is_valid():
                            serializer.save()
                            return onSuccess("Card updated Successfully !!!", serializer.data)
                        else:
                            return badRequest("Something went wrong !!! ")
                    except:
                        return badRequest("Card doesn't exixts !!!")
            else:
                return badRequest("Admin not found !!!")
        else:
            return unauthorisedRequest() 
           
    def delete(self, request):
        token = get_object(request)
        if token:
            get_admin = User.objects.get(id = token["user_id"])
            if get_admin and get_admin.is_admin:
                card_id = request.GET.get("card_id")
                try:
                    card_obj = Card.objects.get(card_id=card_id, user_id=get_admin)
                    card_obj.delete()
                    return onSuccess("Card deleted successfully !!!")
                except:
                    return badRequest("Card doesn't exists")
            else:
                return badRequest("No user found !!!")
        else:
            return unauthorisedRequest()


#-------------------- CREATE, UPDATE USER'S CARD (ADMIN ACCESS) -----------------#

class UserCard(APIView):

    def post(self, request):
        token = get_object(request)
        if token:
            get_admin = User.objects.get(id = token["user_id"])
            if get_admin and get_admin.is_admin:
                data = request.data
                if data["card_bank_name"] != "" and data["card_category"] != "" and data["card_number"] != "" and data["card_network"] != "" and data["card_holder_name"] != "" and data["card_photo"] != "" and data["card_exp_date"] != "" and  data["card_cvv"] != "" and data["due_date"] != "" and data["due_amount"] != "":
                    try:
                        get_user = User.objects.get(id = data["user_id"], under_by = get_admin.id, is_verified = True)
                    except:
                        return badRequest("User is not found or not verified !!!")
                    user_card_number = Card.objects.filter(card_number = data["card_number"])
                    if not user_card_number.exists():
                        data["due_amount"] = "%.2f" % float(data["due_amount"])
                        serializer =  UserCardSerializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                            getCard = Card.objects.get(card_id=serializer.data["card_id"])
                            getCard.profit_amount = getCard.due_amount * getCard.commission/100
                            getCard.profit_amount = "%.2f" % float(getCard.profit_amount)
                            getCard.due_amount = "%.2f" % float(getCard.due_amount)
                            getCard.user_id = get_user
                            getCard.created_by = get_admin
                            getCard.updated_by = get_admin
                            getCard.save()
                            return onSuccess("Card Added Successfully !!!", serializer.data)
                        else:
                            return badRequest("Something went wrong !!!")
                    else:
                        return badRequest("Card already exists !!!")                 
                else:
                    return badRequest("Fields is missing !!!")
            else:
                return badRequest("Admin not found !!!")
        else:
            return unauthorisedRequest()  

    def patch(self, request):
        token = get_object(request)
        if token:
            get_admin = User.objects.get(id = token["user_id"])
            if get_admin and get_admin.is_admin:
                data = request.data
                try:
                    User.objects.get(id = data["user_id"], under_by = get_admin.id, is_verified = True)
                except:
                    return badRequest("User not found !!!")
                try:
                    get_card = Card.objects.get(card_id = data["card_id"])
                except:
                    return badRequest("Card not found !!!s") 
                data["due_amount"] = "%.2f" % float(data["due_amount"])
                serializer = UserCardSerializer(get_card, data=data, partial= True)
                if serializer.is_valid():
                    serializer.save()
                    get_card = Card.objects.get(card_id = serializer.data["card_id"])
                    get_card.profit_amount = get_card.due_amount * get_card.commission / 100
                    get_card.profit_amount = "%.2f" % float(get_card.profit_amount)
                    get_card.updated_by = get_admin
                    get_card.save()
                    return onSuccess("Card Updated Successfully !!!", serializer.data)
                else:
                    return badRequest("Something went wrong !!!")
                           
            else:
                return badRequest("Admin not found !!!")
        else:
            return unauthorisedRequest()
            


            








