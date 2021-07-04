from customUser.models import User
from django.db import models
from doctorsUser.models import DoctorUser

class Rating(models.Model):
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE, related_name='ratingdoc')

    def __str__(self) -> str:
        return f"{self.doctor.fullname} - {self.rating}"
    
