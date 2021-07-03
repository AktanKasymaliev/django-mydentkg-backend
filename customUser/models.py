from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from .decorators import validate_user

class UserManager(BaseUserManager):

    use_in_migrations = True

    @validate_user
    def create_user(self, email, username, password, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    @validate_user
    def create_superuser(self, email, username, password):
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(verbose_name='Имя пользователя', max_length=122)
    email = models.EmailField(_('Email'), unique=True)
    password = models.CharField(verbose_name='Пароль', max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Пример телефоного формата: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'