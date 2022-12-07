
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.http.response import JsonResponse
from meds.models import  Med_type
from meds.models import  User_Medicine
from meds.models import DaysOfWeek
from meds.models import medicine_to_daysOfWeek
from meds.serializers import Med_typeSerializer, User_MedicineSerializer, AllUser_MedicineSerializer, AllDaysOfWeekSerializer
from meds.serializers import MedicineSerializer
from rest_framework import response, status, permissions
from users.models import User


import jwt, datetime

class CreatingMed(APIView):

    def get(self, request):
        #creating med types
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()


        serializer = AllUser_MedicineSerializer(user)
        res = {'success' : True, 'data': serializer.data}

        return response.Response(res)


    def post(self, request):
        jd = request.data

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()


        # check
        if 'name' not in jd or 'type' not in jd or 'time' not in jd:
            res = {'success' : False, 'error' : "not all body requirements are included"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        # creating the
        name = jd['name']
        type = Med_type.objects.filter(med_typeID=int(jd['type']))[0]

        time2 = jd['time'].split(':')
        # make sure there are two items and both are numbers

        if (len(time2) != 2):
            res = {'success' : False, 'error' : "time is not valid format"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        for t in time2:
            if not t.isnumeric():
                res = {'success' : False, 'error' : "time is not valid format"}
                return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        d = datetime.time(int(time2[0]), int(time2[1]), 0)

        val_data = {"user": user.id, "name": name, "type": type.med_typeID, "time": d}

        serializer = User_MedicineSerializer(data=val_data)

        weekDays = []


        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : serializer.errors}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        if type.med_typeID == 2:
            days = jd['days']
            for day in days:
                try:
                    you = DaysOfWeek.objects.get(day_id=day)
                    weekDays.append(you)
                except:
                    res = {'success' : False, 'error' : "day id does not exist"}
                    return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
            for day in weekDays:
                # creating the days of the week
                b = medicine_to_daysOfWeek(day=day, med=User_Medicine.objects.get(usermed_id=serializer.data['usermed_id']))
                b.save()



        res = {'success' : True, 'data' : serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)

    def delete(self, request,id):
        jd = request.data

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        # make sure that that user is logged in

        jd = request.data


        objs = User_Medicine.objects.filter(usermed_id=id, user=user)

        if not objs:
            res = {'success' : False, 'error' : 'object does not exist'}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        objs.delete()

        res = {'success' : True, 'data' : {}}
        return response.Response(res, status=status.HTTP_201_CREATED)

    # provide the id

    def patch(self, request,id):
        jd = request.data

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            you = User_Medicine.objects.get(usermed_id=id)

        except:
            res = {'success' : False, 'error' : "id does not exist"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)


        serializer = User_MedicineSerializer(you,data=jd, partial=True)

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : "invalid body requirements"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data

        an = User_Medicine.objects.get(usermed_id=serializer.data['usermed_id'])

        if 'days' in jd:
            days = jd['days']
            if not days:
                # delete all of the day objects
                med_to_daysObjs = medicine_to_daysOfWeek.objects.filter(med=an)
                for med in med_to_daysObjs:
                    med.delete()



        days = {}
        p = medicine_to_daysOfWeek.objects.filter(med=an)
        for day in p:
            days[int(day.day.day_id)] = day.day.name
        data.update({'days': days})



        res = {'success' : True, 'data': data}
        return response.Response(res, status=status.HTTP_201_CREATED)


class Medicine(APIView):
    def get(self, request, id):
        # getting the medicine with that specific id
        try:
            you = User_Medicine.objects.get(usermed_id=id)

        except:
            res = {'success' : False, 'error' : "id does not exist"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        rr = MedicineSerializer(instance=you)
        data = rr.data

        days = {}
        p = medicine_to_daysOfWeek.objects.filter(med=you)
        for day in p:
            days[int(day.day.day_id)] = day.day.name
        data.update({'days': days})

        res = {'success' : True, 'data': data}
        return response.Response(res)

# getting the types of meds
# this is avaialble to anyone
class MedType(APIView):
    def get(self, request):
        serializer = Med_typeSerializer()
        res = {'success' : True, 'data': serializer.get_med_types()}
        return response.Response(res)


class DaysView(APIView):
    def get(self, request):
        serializer = AllDaysOfWeekSerializer()
        res = {'success' : True, 'data': serializer.get_days()}
        return response.Response(res)
