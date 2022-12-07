from meds.models import  Med_type
from meds.models import  User_Medicine
from rest_framework import serializers


class User_MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Medicine
        fields = ('usermed_id', 'name', 'type', 'time',)

        def create(self,validated_data):
            gender =  Genders.objects.create(**validated_data)
            return gender


    



class Med_typeSerializer(serializers.ModelSerializer):
    med_types = serializers.SerializerMethodField()
    class Meta:
        model = Med_type
        fields = ('med_types',)


    def get_med_types(self):
        print(Med_type.objects.all())
        nums = Med_type.objects.all().values('med_typeID','name')
        return  nums
