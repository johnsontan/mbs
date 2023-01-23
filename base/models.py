from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from PIL import Image
from django.utils import timezone, dateformat

class UserManager(BaseUserManager):
    """ User Manager that knows how to create users via email instead of username """
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

class userInfo(AbstractUser):
    object = UserManager()
    CUSTOMER = 1
    EMPLOYEE = 2
    ASSISTANT = 3
    MANAGER = 4

    ROLE_CHOICES = {
        (CUSTOMER, 'Customer'),
        (EMPLOYEE, 'Employee'),
        (ASSISTANT, 'Assistant'),
        (MANAGER, 'Manager')
    }

    username = None
    email = models.EmailField("email address", blank=False, null=False, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    role = models.PositiveBigIntegerField(choices=ROLE_CHOICES, blank=False, null=False, default="1")
    dob = models.DateField(blank=False, null=False)
    phone = models.CharField(max_length=8, unique=True)
    is_suspend = models.BooleanField(default=0)

    def __str__(self):
        return f'{self.email}'

class profile_pic(models.Model):
    user=models.OneToOneField(userInfo, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.email} profile pic'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500,500)
            img.thumbnail(output_size)
            img.save(self.image.path)

class contact(models.Model):
    name = models.CharField(max_length=250 ,blank=False, null=False)
    cemail = models.EmailField(blank=False, null=False)
    cphone = models.CharField(max_length=8)
    message = models.TextField(blank=False, null=False)
    is_ack = models.BooleanField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        datevalue = dateformat.format(self.created_at, 'd b Y')
        return f'{self.name} message at {datevalue}'



