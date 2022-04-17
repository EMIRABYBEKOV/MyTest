from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class MyAccountManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_default_profile_image():
    return "profile_images/profile-default-img.jpeg"

def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.pk) + '/profile_image.png'

class MyAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(blank=True, null=True, default=get_default_profile_image,
                                      upload_to=get_profile_image_filepath)

    USERNAME_FIELD = 'username'

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

