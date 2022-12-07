from django.db import models
from users.models import User
from django.shortcuts import render


# creating the med_type
class Med_type(models.Model):
    med_typeID = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='type_id'
        )
    name = models.CharField(max_length=1000, null=True)
    class Meta:
        db_table = 'Med_type'



# these are all of the medicines that each user creates
class User_Medicine(models.Model):
    usermed_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='med_id'
        )

    user = models.ForeignKey(
         User,
         on_delete=models.CASCADE,
         verbose_name='user',
         null=True,
    )

    # the name of the medicine
    name = models.CharField(max_length=1000, null=True)

    type = models.ForeignKey(
         Med_type,
         on_delete=models.CASCADE,
         verbose_name='type',
         null=True,
    )

    #this contains the time that the medicine must be taken in
    time = models.TimeField(null=True)

    class Meta:
        db_table = 'User_Medicine'
