from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework import response, status, permissions
from users.models import User
from datetime import date
from meds.models import  User_Medicine
from .serializers import MedicineTimelineSerializer
from .models import Taken_medicine
import datetime

import jwt
from django.utils import timezone
from datetime import timedelta


class TimeLineView(APIView):
    #
    def get(self, request):

        # get the user via cookies
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        # get all of the pills
        p = User_Medicine.objects.order_by().filter(user=user)

        rr = MedicineTimelineSerializer(instance=p)

        today = date.today()
        d2 = today.strftime("%B %d")
        x = today.isoweekday()
        print(today)
        print(d2)
        print(x)

        res = {'success' : True, 'data': rr.data}
        return response.Response(res)

class TakeMedicineInTimelineView(APIView):

    def post(self, request, id):


        # get the user via cookies
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        # get the medicine object with the id of the logged in user and id
        meds = User_Medicine.objects.filter(user=user, usermed_id=id)

        if not meds:
            res = {'success' : False, 'error' : "no medicine found with that id "}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        med = meds[0]

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        # today = date.today()
        # TODO

        # today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        # today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        #
        # n = Taken_medicine.objects.get(created_at__range=(today_min, today_max), usermed_id = med.usermed_id)
        #
        # print(n.)

        # medicineToTake =


        res = {'success' : True, 'data': {}}
        return response.Response(res)
