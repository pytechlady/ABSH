from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Appointment
from .serializers import AppointmentSerializer, GetAppointmentSerializer
from users.models import User
from .utils import Util


# Create your views here.
class Appointments(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    queryset = Appointment.objects.all()

    @action(methods=["POST"], detail=False, serializer_class=AppointmentSerializer)
    def book_appointment(self, request):
        try:
            user = request.user

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, is_completed=False)
                return Response(
                    {
                        "message": "Appointment booked successfully",
                        "success": True,
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "message": "Appointment was not booked",
                        "success": False,
                        "data": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            print(str(e))
            return Response(
                {
                    "message": "Error processing appointment request",
                    "success": False,
                    "data": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
    @action(methods=['GET'], detail=False)
    def get_appointment(self, request):
        try:
            appointment = Appointment.objects.get(id=request.GET.get('id'))
            if appointment:
                serializer = self.get_serializer(appointment)
                return Response({'success': True, "message": "Appointment successfully retrieved", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({'success': False, "message": "Appointment not found", "data": None}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, "message": "Error while getting appointment", "data": None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=["PATCH"], detail=False, serializer_class=AppointmentSerializer)
    def update_appointment(self, request):
        try:
            appointment = Appointment.objects.filter(id=request.GET.get("id")).first()
            if appointment:
                serializer = self.get_serializer(
                    appointment, data=request.data, partial=True
                )
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(
                        {
                            "message": "Appointment updated successfully",
                            "success": True,
                            "data": serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"message": "Appointment not updated", "success": False},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"message": "Appointment not found", "success": False},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                {"message": "Appointment not updated", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(methods=["GET"], detail=False, serializer_class=GetAppointmentSerializer)
    def get_all_appointments(self, request):
        try:
            appointments = Appointment.objects.all(ordering=["-appointment_date"])
            serializer = self.get_serializer(appointments, many=True)
            return Response(
                {
                    "message": "Appointments retrieved successfully",
                    "success": True,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "Appointments not retrieved", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(methods=["GET"], detail=False, serializer_class=GetAppointmentSerializer)
    def get_a_patient_appointments(self, request):
        try:
            pending = []
            completed = []
            user = request.user
            if user:
                appointments = Appointment.objects.filter(user=user)
                serializer = self.get_serializer(appointments, many=True)
                for appointment_data in serializer.data:
                    if appointment_data["is_completed"]:
                        completed.append(appointment_data)
                    else:
                        pending.append(appointment_data)
                return Response(
                    {
                        "message": "Appointments retrieved successfully",
                        "success": True,
                        "data": serializer.data,
                        "count": len(serializer.data),
                        "pending": len(pending),
                        "completed": len(completed),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "User not found", "success": False},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                {"message": "Appointments not retrieved", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(methods=["GET"], detail=False, serializer_class=GetAppointmentSerializer)
    def get_a_doctor_appointments(self, request):
        try:
            pending = []
            completed = []
            doctor = request.user

            if doctor:
                appointments = Appointment.objects.filter(doctor=doctor.id)
                serializer = self.get_serializer(appointments, many=True)

                for appointment_data in serializer.data:
                    if appointment_data["is_completed"]:
                        completed.append(appointment_data)
                    else:
                        pending.append(appointment_data)

                return Response(
                    {
                        "message": "Appointments retrieved successfully",
                        "success": True,
                        "data": serializer.data, 
                        "pending": len(pending),
                        "completed": len(completed),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Doctor not found", "success": False},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                {"message": "Appointments not retrieved", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(methods=["DELETE"], detail=False, serializer_class=AppointmentSerializer)
    def delete_appointment(self, request):
        try:
            appointment = Appointment.objects.filter(id=request.GET.get("id")).first()
            if appointment:
                appointment.delete()
                return Response(
                    {"message": "Appointment deleted successfully", "success": True},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Appointment not found", "success": False},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                {"message": "Appointment not deleted", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
