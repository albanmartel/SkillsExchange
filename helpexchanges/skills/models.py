from django import forms
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.db import models
from datetime import date, datetime, timedelta

from django.db.models.fields import related
from django.utils.translation import gettext_lazy as _

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

class AssistanceType(models.TextChoices):
    """
    AssistanceType model
    ENUM class
    Implementing an enum class in Django
    for the type of help
    """
    OFFER = "OFFER", _("offer of help")
    REQUEST = "REQUEST", _("request for help")

class AssistanceStatus(models.TextChoices):
    """
    AssistanceStatus model
    ENUM class
    Implementing an enum class in Django
    for the status of Assistance event.
    """
    OPEN = "OPEN", _("Open")
    CANCELLED = "CANCELLED", _("Cancelled")
    EXPIRED = "EXPIRED", _("Expired")

class Assistance(models.Model):
    """
    Assistance model
    """
    id_assistance = models.AutoField(primary_key=True)
    # link to CustomUser Model
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="offer_activities", null=True, blank=True,
    )
    # Link to Activity Model
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="request_activities"
    )
    assistance_type = models.CharField (
        max_length=16,
        choices=AssistanceType,
        default=AssistanceType.OFFER,
    )
    assistance_status = models.CharField(
        max_length=16,
        choices=AssistanceStatus,
        default=AssistanceStatus.OPEN
    )
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

    def __str__(self) -> str:
        if self.activity:
            dt_local = timezone.localtime(self.start_date_time)
            date_locale = dt_local.date()
            start_time = dt_local.time()
            dt_local = timezone.localtime(self.end_date_time)
            end_time = dt_local.time()
            return f"{self.pk}: {self.assistance_type} {self.author.username}, Activity:{self.activity.activity_title}, Date:{date_locale}, Start: {start_time} End:{end_time})"
        return f"Assistance #{self.pk}"


class Appointment(models.Model):
    assistance= models.ForeignKey(
        Assistance,
        on_delete=models.CASCADE,
        related_name='appointment',
        verbose_name='appointment assistance'
    )
    # the other user, the one who did not create the support slot
    partner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='partner',
        verbose_name='partner of assistance',
        null=True,
        blank=True,
    )
    id_appointment_activity = models.AutoField(primary_key=True)
    is_confirmed = models.BooleanField(default=False)
    isConfirmedByOfferer = models.BooleanField(
        default=False,
        verbose_name="is then appointment is confirmed"
    )
    # create a date that is null by default
    # https://stackoverflow.com/a/53721823
    confirmationDateTime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="date and time of the appointment confirmation"
    )

    def set_confirmed(self) -> None:
        self.is_confirmed = True
        if self.confirmation_datetime is None:
            self.confirmation_datetime = timezone.now()
        self.save(update_fields=["is_confirmed", "confirmation_datetime"])



