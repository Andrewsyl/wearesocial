from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone


# Create your models here.

class AccountUserManager(UserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    stripe_id = models.CharField(max_length=40, default='')
    subscription_end = models.DateTimeField(default=timezone.now())
    hometown = models.CharField(max_length=50)
    bio = models.TextField(max_length=500, blank=True)
    # age = models.IntegerField()
    image = models.ImageField(upload_to="images", blank=True, null=True)
    objects = AccountUserManager()

'''class UserProfile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=50)
    hometown = models.CharField(max_length=50)
    #age = models.IntegerField()
    image = models.ImageField(upload_to="images", blank=True, null=True)'''

User.profile = property(lambda u: User.objects.get_or_create(user=u)[0])
