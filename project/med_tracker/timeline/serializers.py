from meds.models import  Med_type
from meds.models import  User_Medicine
from meds.models import DaysOfWeek
from rest_framework import serializers

from meds.models import medicine_to_daysOfWeek


class MedicineTimelineSerializer(serializers.ModelSerializer):
    fullday =  serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    timeline = serializers.SerializerMethodField()


    class Meta:
        model = User_Medicine
        fields = '__all__'

    def get_timeline(self, obj):
        rr = []
        for an in obj:
            nObj = {}
            nObj['id'] = an.usermed_id
            nObj['name'] = an.name
            nObj['time'] = an.time
            rr.append(nObj)
        return rr

    def get_fullday(self, obj):
        return "Thursday"

    def get_date(self, obj):
        return  "december 8"
