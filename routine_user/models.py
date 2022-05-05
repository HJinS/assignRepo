from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager
import uuid


class RoutineUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    email = models.EmailField(_('email address'), unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
