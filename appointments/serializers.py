from rest_framework import serializers
from .models import Appointment




class AppointmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Appointment
        fields = ('id', 'doctor', 'scheduled_time', 'appointment_reason', 'is_completed')
        read_only_fields = ('id', 'created_at', 'updated_at')
        
        
class GetAppointmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Appointment
        fields = ('id', 'user', 'doctor', 'scheduled_time', 'appointment_reason', 'is_completed')
        