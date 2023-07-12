# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
# import sys
#
## assuming your django settings file is at '/home/pratikScalelot/mysite/mysite/settings.py'
# and your manage.py is is at '/home/pratikScalelot/mysite/manage.py'
# path = '/c/Users/scale/Desktop/Final Credit/creditmanagement'
# if path not in sys.path:
#     sys.path.append(path)
#
os.environ['DJANGO_SETTINGS_MODULE'] = 'creditmanagement.settings'
#
## then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



# """
# WSGI config for creditmanagement project.

# It exposes the WSGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
# """

# import os
# import sys
# from django.conf import settings    
# # from decouple import config

# from django.core.wsgi import get_wsgi_application

# # path = r'C:\Users\scale\Desktop\Final Credit\creditmanagement'
# # if path not in sys.path:
# #     sys.path.append(path)

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'creditmanagement.creditmanagement.settings')

# application = get_wsgi_application()

# # from whitenoise import WhiteNoise
# # application = DjangoWhiteNoise(application)



