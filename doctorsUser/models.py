from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _  
from django.utils import timezone

from customUser.decorators import validate_user

User = get_user_model()

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
    license_image = models.ImageField(upload_to='licenses', verbose_name='Лицензия')
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

class Reception(models.Model):
    client_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="reception")
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE, related_name='time')
    from_to = models.TimeField(verbose_name='От')
    to = models.TimeField(verbose_name="До")
    date = models.DateField(verbose_name='Дата приема')

    class Meta:
        db_table = 'reciption'
        verbose_name = 'Прием врача'
        verbose_name_plural = 'Приемы врачей'

class Reserve(models.Model):
    
    who = models.ForeignKey(verbose_name="Клиент", to=User, on_delete=models.CASCADE, related_name='who')
    doctor = models.ForeignKey(verbose_name="Доктор", to=DoctorUser, on_delete=models.CASCADE, related_name='reserve')
    from_to = models.TimeField(verbose_name='Забранированно От', default="18:30:18")
    to = models.TimeField(verbose_name="Забранированно До", default="19:30:18")
    date = models.DateField(verbose_name='Забранированная дата', default="2021-08-13")

    class Meta:
        db_table = 'reserver'
        verbose_name = 'Забронированное время'
        verbose_name_plural = 'Забронированные времена'