from meds.models import  Med_type
from meds.models import  User_Medicine
from meds.models import DaysOfWeek
from rest_framework import serializers
from django.db import models
from django.shortcuts import render



class Taken_medicine(models.Model):
    usermed_id = models.ForeignKey(
         User_Medicine,
         on_delete=models.CASCADE,
         verbose_name='med',
         null=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
