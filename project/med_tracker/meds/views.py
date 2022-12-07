
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.http.response import JsonResponse
from meds.models import  Med_type
from meds.models import  User_Medicine
from meds.serializers import Med_typeSerializer
from rest_framework import response, status, permissions


import jwt, datetime


class CreatingMed(APIView):
    def get(self, request):
        #creating med types
        serializer = Med_typeSerializer()

        res = {'success' : True, 'data': serializer.get_med_types()}

        return response.Response(res)

# getting the types of meds
class MedType(APIView):
    def get(self, request):
        datos = {'codigo':"200",'message': "Users not found..."}
        return JsonResponse(datos)
