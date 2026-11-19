from django import forms
from django.contrib.auth import admin
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.

class Skill(models.Model):
    """
    Skill model
    This model corresponds to the Skill class.
    This class allows several activities representing it to be grouped together
    """
    idSkill = models.AutoField(primary_key=True)
    skillName = models.CharField(max_length=100, unique=True, verbose_name="Name of Skill")
    description = models.TextField

    def __str__(self):
        return self.skillName
