from django.db import models
from customUser.models import User
from doctorsUser.models import DoctorUser

class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE, related_name='doctor')
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    class Meta:
        db_table = "comments"
        verbose_name = 'Комментарий'
        verbose_name_plural = "Комментарии"
