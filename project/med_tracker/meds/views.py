
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.http.response import JsonResponse
from meds.models import  Med_type
from meds.models import  User_Medicine
import jwt, datetime




class CreatingMed(APIView):
    def get(self, request):
        datos = {'codigo':"200",'message': "Users not found..."}

        return JsonResponse(datos)
