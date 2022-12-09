from meds.models import  Med_type
from meds.models import  User_Medicine
from meds.models import DaysOfWeek
from .models import Medicine_taken
from rest_framework import serializers

from meds.models import medicine_to_daysOfWeek
from datetime import date
import datetime


class MedicineTimelineSerializer(serializers.ModelSerializer):
    fullday =  serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    timeline = serializers.SerializerMethodField()


    class Meta:
        model = User_Medicine
        fields = ('fullday', 'date','timeline',)

    def get_timeline(self, obj):
        today = date.today()
        x = today.isoweekday()
        type = {2:'Every other day', 1:'Daily'}
        rr = []
        for an in obj:

            # getting the days
            if an.type.med_typeID == 2:
                nObj = {}
                nObj['id'] = an.usermed_id
                nObj['name'] = an.name
                nObj['time'] = an.time
                nObj['type'] = type[an.type.med_typeID]
                nObj['quantity'] = 1
                nObj['taken'] = True

                # setting th taken functionality
                today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
                today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

                try:
                    n = Medicine_taken.objects.get(created_at__range=(today_min, today_max), usermed_id = an.usermed_id)

                except:
                    nObj['taken'] = False


                isValid = False

                days = []
                # get all of the days that the medicine has
                dayObjs = medicine_to_daysOfWeek.objects.filter(med=an.usermed_id)
                for day in dayObjs:
                    if day.day.day_id == x:
                        isValid = True
                    days.append(day.day.name)
                nObj['days'] = days
                if isValid:
                    rr.append(nObj)

            else:
                nObj = {}
                nObj['id'] = an.usermed_id
                nObj['name'] = an.name
                nObj['time'] = an.time
                nObj['type'] = type[an.type.med_typeID]
                nObj['quantity'] = 1
                nObj['taken'] = True
                # setting th taken functionality
                today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
                today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

                try:
                    n = Medicine_taken.objects.get(created_at__range=(today_min, today_max), usermed_id = an)

                except:
                    nObj['taken'] = False




                rr.append(nObj)

        return rr

    def get_fullday(self, obj):
        days = {1:"Monday", 2: "Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday", 7:"Sunday"}
        today = date.today()
        x = today.isoweekday()
        return days[x]

    def get_date(self, obj):
        today = date.today()
        d2 = today.strftime("%B %d")
        return  d2
