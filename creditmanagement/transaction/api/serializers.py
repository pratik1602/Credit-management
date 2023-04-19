from rest_framework import serializers
from usercredit.models import *

class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"