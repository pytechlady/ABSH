from django.db import models
from users.models import User

# Create your models here.
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
    scheduled_time = models.DateTimeField(blank=True, null=True)
    appointment_reason = models.CharField(max_length=255, blank=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.doctor.first_name} {self.doctor.last_name}'
    
    
