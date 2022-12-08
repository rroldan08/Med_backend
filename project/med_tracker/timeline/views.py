from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework import response, status, permissions
from users.models import User
from datetime import date
from meds.models import  User_Medicine
from .serializers import MedicineTimelineSerializer

import jwt

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

        print(p)

        rr = MedicineTimelineSerializer(instance=p)
        # print()




        today = date.today()
        d2 = today.strftime("%B %d")
        x = today.isoweekday()
        print(today)
        print(d2)
        print(x)



        res = {'success' : True, 'data': rr.data}
        return response.Response(res)
