import math
import random
from django.core.cache import cache

def generate_ref_code() :
        
    digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    REFERCODE = ""
    for i in range(6) :
        REFERCODE += digits[math.floor(random.random() * 62)]
    return REFERCODE

