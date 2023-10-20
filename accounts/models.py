from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    # 자기 자신과 다대다 관계, 대칭은 아님, 역참조시 이름 followers