from meds.models import  Med_type
from meds.models import  User_Medicine
from meds.models import DaysOfWeek
from rest_framework import serializers
from django.db import models
from django.shortcuts import render



class Taken_medicine(models.Model):
    usermed_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='med_id'
        )
    created_at = models.DateTimeField(auto_now_add=True)
