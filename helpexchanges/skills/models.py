from django import forms
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from datetime import date, datetime, timedelta

class Skill(models.Model):
    """
    Skill model
    This model corresponds to the Skill class.
    This class allows several activities representing it to be grouped together
    """
    id_skill = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=100, unique=True, verbose_name="Skill Name")
    skill_description = models.TextField(verbose_name="Skill Description")

    def __str__(self):
        return self.skill_name

class CustomUser(AbstractUser):
    """
    CustomUser model
    This template allows the user to customise the traditional Django class.
    In this case, the ‘phone’ and ‘biography’ parameters are added.
    For this to work, certain requirements must be met, particularly in the ‘settings.py’ file.
    """
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField(
        Skill,
        related_name="users",
        blank=True
    )

    class Meta:
        ordering = ['username']


class Activity(models.Model):
    """
    Activity model
    This model corresponds to the Activity class.
    This class will be used to facilitate the exchange of activities
    """
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name='activities', blank=True, null=True
    )
    id_activity = models.AutoField(primary_key=True)
    activity_title = models.CharField(max_length=100, unique=True, verbose_name="Title of Activity")
    activity_description = models.TextField(blank=True, verbose_name="Description of Activity")

    def __str__(self):
        return self.activity_title


class EventActivityModel(models.Model):
    """
    EventActivityModel model
    parentclass of the 'requestactivity', 'offeractivity' and 'appointmentactivity' classes
    """
    start_date_time = models.DateTimeField(verbose_name="Date and time of beginning")
    end_date_time = models.DateTimeField(verbose_name="Date and time of end")
    # How can I ensure that, when the record is created, the date used is today’s date?
    # https://stackoverflow.com/a/2771701
    creationDateTime = models.DateTimeField(
        default=datetime.now,
        blank=True,
        verbose_name = "Date and time of now"
    )

    def get_duration(self):
        """
        the code is inspired by  : https://stackoverflow.com/a/10981895
        """
        if not self.start_date_time or not self.end_date_time:
            return None

        delta = self.end_date_time - self.start_date_time
        if delta.total_seconds() < 0:
            return None

        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        return {
            "days": delta.days,
            "hours": hours,
            "minutes": minutes,
        }

    def get_start_date_time(self):
        return self.start_date_time

    def get_end_date_time(self):
        return self.end_date_time

    def set_start_date_time(self, start_datetime):
        self.start_date_time = start_datetime

    def set_end_date_time(self, end_datetime):
        self.end_date_time = end_datetime

    class Meta:
        abstract = True

class RequestActivity(EventActivityModel):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="request_activities"
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="request_activities", null=True, blank=True,
    )
    id_request_activity = models.AutoField(primary_key=True)

    def get_user(self):
        #self.activity.skill.
        pass

class OfferActivity(EventActivityModel):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="offer_activities"
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="offer_activities", null=True, blank=True,
    )
    id_offer_activity = models.AutoField(primary_key=True)

class AppointmentActivity(EventActivityModel):
    offer_activity = models.ForeignKey(
        OfferActivity, on_delete=models.CASCADE, related_name='appointement_offer_activity'
    )
    request_activity = models.ForeignKey(
        RequestActivity, on_delete=models.CASCADE, related_name='appointement_offer_activity', null=True, blank=True,
    )
    id_appointment_activity = models.AutoField(primary_key=True)
    isConfirmedByOfferer = models.BooleanField(default=False, verbose_name="is then appointment is confirmed")
    # create a date that is null by default
    # https://stackoverflow.com/a/53721823
    confirmationDateTime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="date and time of the appointment confirmation"
    )



