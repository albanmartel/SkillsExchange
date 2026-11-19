from django import forms
from django.contrib.auth import admin
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import date, datetime, timedelta

# Create your models here.

class Skill(models.Model):
    """
    Skill model
    This model corresponds to the Skill class.
    This class allows several activities representing it to be grouped together
    """
    id_skill = models.AutoField(primary_key=True)
    skill_Name = models.CharField(max_length=100, unique=True, verbose_name="Name of Skill")
    skill_description = models.TextField

    def __str__(self):
        return self.skill_name

class Activity(models.Model):
    """
    Activity model
    This model corresponds to the Activity class.
    This class will be used to facilitate the exchange of activities
    """
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name='skill', blank=True, null=True
    )
    id_activity = models.AutoField(primary_key=True)
    activity_title = models.CharField(max_length=100, unique=True, verbose_name="Title of Activity")
    activity_description = models.TextField

    def __str__(self):
        return self.activity_title


class EventActivity(models.Model):
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()

    def __init__(self, start_datetime, end_datetime):
        self.start_date_time = start_datetime
        self.end_date_time = end_datetime

    def difference(self):
        difference = self.end_date_time - self.start_date_time

        years = difference.days // 365
        days = difference.days
        hours = difference.hours
        minutes = difference.minutes

        return { 'years': years, 'days': days, 'hours': hours, 'minutes': minutes }

    def get_start_date_time(self):
        return self.start_date_time

    def get_end_date_time(self):
        return self.end_date_time

    def set_start_date_time(self, start_datetime):
        self.start_date_time = start_datetime


    def set_end_date_time(self, end_datetime):
        self.end_date_time = end_datetime








