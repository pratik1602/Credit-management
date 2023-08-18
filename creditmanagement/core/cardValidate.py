from django.core.exceptions import ValidationError
from rest_framework.response import Response

##### VALIDATION FUNCTIONS ########

def validate_cvv(card_cvv):
    cvv = str(card_cvv)
    if len(cvv) >  3 and len(cvv) >  4:
        raise ValidationError ("card cvv is not more than 3 or 4 numbers !!!")
    elif len(cvv) < 3:
        raise ValidationError ("card cvv is not less than 3  numbers !!!")
  

def validate_card_number(card_number):

    number = list(str(card_number).strip())

    check_digit = number.pop()

    number.reverse()

    processed_digits = []

    for index, digit in enumerate(number):
        if index % 2 == 0:
            doubled_digit = int(digit) * 2

            if doubled_digit > 9:
                doubled_digit = doubled_digit - 9
            processed_digits.append(doubled_digit)
        else:
            processed_digits.append(int(digit))

    total = int(check_digit) + sum(processed_digits)

    if total % 10 == 0:
        return Response(True)
    else:
        raise ValidationError ("card Number is Invalid !!!")


from datetime import datetime
date = datetime.today().date()

def is_expired(card_exp_date):

    if card_exp_date <  date:
        raise ValidationError("Card is expired !!!")

def has_expired(due_date):

    if due_date < date:
        raise ValidationError("You can not enter past date !!!")
    

# getting the type of card
# if 1st number 
# 4 - visa
# 5 - master card
# 37 - american express
# 6 - discovery card 

def card_type(card_number):
    if card_number[:1] == "4":
        return "visa card"
    elif card_number[:1] == "5":
        return "master card"
    elif card_number[:2] == "37":
        return "american express card"
    elif card_number[:1] == "6":
        return "discovery card"
    else:
        return "unknown card"
# print(card_type)
        

