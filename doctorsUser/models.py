from django.db import models

from customUser.models import User
from django.utils.translation import ugettext_lazy as _

class DoctorUser(User):

    fullname = models.CharField(verbose_name='Ф.И.О', max_length=500)

    avatar = models.ImageField(upload_to='docs_avatars', verbose_name='Аватар')
    profession = models.CharField(verbose_name='Профессия врача', max_length=255)
    experience = models.CharField(verbose_name='Стаж', max_length=100)
    price = models.PositiveIntegerField(verbose_name='Цена приема')
    company = models.CharField(verbose_name='Компания', max_length=255)
    address = models.CharField(verbose_name='Адрес', max_length=500)


    def __str__(self) -> str:
        return f"Доктор {self.fullname}"
        

    class Meta:
        db_table = 'doctors_user'
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'
