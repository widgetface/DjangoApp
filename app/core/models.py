from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

# provides helper functions for creation of a user


class UserManager(BaseUserManager):

    # Any argumants passed in bsides email , password
    # are put into **extra_fields
    def create_user(self, email, password=None, **extra_fields):
        """ Create and saves a new user """
        if not email:
            raise ValueError('users must have an email address')
        # self.normalize_email lowercases letters after '@' in email
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        # pass password which is encrypted
        # using set_password helper function
        user.set_password(password)
        # Good prcatice to save the password
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        """ Create and save new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email instead of username """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
