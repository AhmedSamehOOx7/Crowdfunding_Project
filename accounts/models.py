from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    mobile_phone = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^01[0125][0-9]{8}$',
                message='Enter a valid Egyptian mobile number.'
            )
        ],
        unique=True
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
