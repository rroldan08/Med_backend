from meds.models import  Med_type
from meds.models import  User_Medicine
from rest_framework import serializers


class Med_typeSerializer(serializers.ModelSerializer):
    med_types = serializers.SerializerMethodField()
    class Meta:
        model = Med_type
        fields = ('med_types',)


    def get_med_types(self):
        print(Med_type.objects.all())
        nums = Med_type.objects.all().values('med_typeID','name')
        return  nums
