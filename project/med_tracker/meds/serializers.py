from meds.models import  Med_type
from meds.models import  User_Medicine
from meds.models import DaysOfWeek
from rest_framework import serializers

from meds.models import medicine_to_daysOfWeek


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
        fields = ('user_medicine',)

    def add(self, key, value):
        self[key] = value
    # this is to get all of the
    def get_user_medicine(self, obj):
        nums = User_Medicine.objects.all().filter(user=obj).values('usermed_id','name', 'type', 'time',)
        # nums[0]['angel'] = "angel"
        nums[0].update()
        print()
        for num in nums:
            days = {}
            an = User_Medicine.objects.get(usermed_id=num['usermed_id'])
            p = medicine_to_daysOfWeek.objects.filter(med=an)
            for day in p:
                days[int(day.day.day_id)] = day.day.name
            num.update({'days': days})
        return nums



class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Medicine
        fields = '__all__'


class Med_typeSerializer(serializers.ModelSerializer):
    med_types = serializers.SerializerMethodField()
    class Meta:
        model = Med_type
        fields = ('med_types',)

    def get_med_types(self):
        print(Med_type.objects.all())
        nums = Med_type.objects.all().values('med_typeID','name')
        return  nums

# serializer for getting all of the days


class AllDaysOfWeekSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField()
    class Meta:
        model = DaysOfWeek
        fields = ('days', )

    # this is to get all of the
    def get_days(self):
        meds = DaysOfWeek.objects.all().values('day_id', 'name',)
        return meds
