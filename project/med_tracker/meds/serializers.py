from meds.models import  Med_type
from meds.models import  User_Medicine
from rest_framework import serializers


class User_MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Medicine
        fields = ('usermed_id', 'name', 'type', 'time','user',)

        def create(self,validated_data):
            gender =  User_Medicine.objects.create(**validated_data)
            return gender

# this is the serializer to get all of the medicines that belong to a user
class AllUser_MedicineSerializer(serializers.ModelSerializer):
    user_medicine = serializers.SerializerMethodField()
    class Meta:
        model = User_Medicine
        fields = ('user_medicine', )

    # this is to get all of the
    def get_user_medicine(self, obj):
        nums = User_Medicine.objects.all().filter(user=obj).values('name', 'type', 'time',)
        return nums


class Med_typeSerializer(serializers.ModelSerializer):
    med_types = serializers.SerializerMethodField()
    class Meta:
        model = Med_type
        fields = ('med_types',)

    def get_med_types(self):
        print(Med_type.objects.all())
        nums = Med_type.objects.all().values('med_typeID','name')
        return  nums
