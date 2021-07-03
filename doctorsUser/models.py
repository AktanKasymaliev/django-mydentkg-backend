from customUser.decorators import validate_user
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from customUser.models import User
from django.utils.translation import ugettext_lazy as _

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

class DoctorUser(User):

    fullname = models.CharField(verbose_name='Ф.И.О', max_length=500)

    avatar = models.ImageField(upload_to='docs_avatars', verbose_name='Аватар', blank=True, null=True)
    profession = models.CharField(verbose_name='Профессия врача', max_length=255)
    experience = models.CharField(verbose_name='Стаж', max_length=100)
    price = models.PositiveIntegerField(verbose_name='Цена приема')
    company = models.CharField(verbose_name='Компания', max_length=255)
    address = models.CharField(verbose_name='Адрес', max_length=500)

    objects = UserManager()

    def __str__(self) -> str:
        return f"Доктор {self.fullname}"
        

    class Meta:
        db_table = 'doctors_user'
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'
