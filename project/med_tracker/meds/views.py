
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.http.response import JsonResponse
from meds.models import  Med_type
from meds.models import  User_Medicine
from meds.serializers import Med_typeSerializer, User_MedicineSerializer, AllUser_MedicineSerializer

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



        serializer = AllUser_MedicineSerializer()
        res = {'success' : True, 'data': serializer.get_user_medicine(obj=user)}

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
        time = jd['time']

        val_data = {"user": user.id, "name": name, "type": type.med_typeID, "time": time}

        serializer = User_MedicineSerializer(data=val_data)


        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : serializer.errors}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)


        res = {'success' : True, 'data' : serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)



# getting the types of meds
# this is avaialble to anyone
class MedType(APIView):
    def get(self, request):
        serializer = Med_typeSerializer()
        res = {'success' : True, 'data': serializer.get_med_types()}
        return response.Response(res)
