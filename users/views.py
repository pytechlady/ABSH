from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer, UserProfileSerializer, AuthenticationSerializer, DocAuthenticationSerializer, DocSerializer

# Create your views here.

class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    
    @action(methods=['POST'], detail=False, serializer_class=UserSerializer)
    def register_patients(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True, 'data': serializer.data, 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['PATCH'], detail=False, serializer_class=UserProfileSerializer)
    def update_user_details(self, request):
        try:
            current_user = request.user
            user = User.objects.filter(id=current_user.id).first()
            if user:
                serializer = self.get_serializer(user, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({'message': 'User details updated successfully', 'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'User details not updated', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'User not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    @action(methods=['GET'], detail=False, serializer_class=UserProfileSerializer)
    def get_all_patients(self, request):
        try:
            users = User.objects.filter(is_active=True)
            if users:
                serializer = self.get_serializer(users, many=True)
                return Response({'message': 'Patients retrieved successfully', 'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No patients found', 'success': False}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(methods=['GET'], detail=False, serializer_class=UserProfileSerializer)
    def get_a_patient(self, request):
        try:
            user = User.objects.filter(id=request.GET.get('id')).first()
            if user:
                serializer = self.get_serializer(user)
                return Response({'message': 'Patient retrieved successfully', 'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Patient not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(methods=['DELETE'], detail=False, serializer_class=UserProfileSerializer)
    def delete_a_patient(self, request):
        try:
            user = User.objects.filter(id=request.GET.get('id')).first()
            if user:
                user.is_active = False
                return Response({'message': 'Patient deleted successfully', 'success': True}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Patient not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

class AuthenticationViewset(viewsets.ModelViewSet):
    serializer_class = AuthenticationSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    
    @action(methods=['POST'], detail=False, serializer_class=AuthenticationSerializer)
    def user_login(self, request):
        username = request.data['username']
        password = request.data['password']
        
        if username is None and password is None:
            return Response({'message': "invalid_credentials.Please provide both username and password", "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        user = authenticate(username=username, password=password)
        if not user:
                return Response({"message": "Invalid credentials", "success": False},
                    status=status.HTTP_404_NOT_FOUND,
                )
                
        elif user.is_doctor == True:
            return Response({'message': 'Kindly login from the doctors section', 'success': False},
                            status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"message": "Logged in successfully", "success": True, "data": {
            "token": token.key, "id": user.id}}, status=status.HTTP_200_OK)
        

class DoctorViewset(viewsets.ModelViewSet):
    serializer_class = DocSerializer
    queryset = User.objects.all()
    http_method_names = ['post', 'patch', 'get', 'delete']

    @action(methods=['POST'], detail=False)
    def register_doctor(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'data': serializer.data, 'message': 'Doctor account created successfully'}, status=status.HTTP_201_CREATED)
        except ValidationError as validation_error:
            return Response({'success': False, 'data': None, 'message': str(validation_error)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as integrity_error:
            return Response({'success': False, 'data': None, 'message': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'data': None, 'message': f'Error creating account: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                
    @action(methods=['GET'], detail=False)
    def get_all_doctors(self, request):
        try:
            doctors = User.objects.filter(is_doctor=True)
            if doctors:
                serializer = self.get_serializer(doctors, many=True)
                return Response({'message': 'Doctors retrieved successfully', 'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No Doctors found', 'success': False}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(methods=['GET'], detail=False)
    def get_doctor(self, request):
        try:
            doctor = User.objects.filter(id=request.GET.get('id')).first()
            if doctor:
                serializer = self.get_serializer(doctor)
                return Response({'message': 'Doctor retrieved', 'success': True, 'data': serializer.data }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No doctor found', 'success': False, 'data': serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'message': 'Doctor not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as err:
            return Response({'message': str(err), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class DocAuthenticationViewSet(viewsets.ModelViewSet):
    serializer_class = DocAuthenticationSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    
    @action(methods=['POST'], detail=False)
    def doc_login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username is None or password is None:
            return Response({'message': 'Invalid credentials. Please provide both username and password', 'success': False},
                            status=status.HTTP_400_BAD_REQUEST)

        # Authenticate against the Doctor model
        user = authenticate(username=username, password=password)

        if not user:
            return Response({'message': 'Invalid username or password', 'success': False},
                            status=status.HTTP_400_BAD_REQUEST)
        elif user.is_doctor == False:
            return Response({'message': 'You are not authorized to login as a doctor', 'success': False},
                            status=status.HTTP_401_UNAUTHORIZED)

        # If authentication is successful, generate a token
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"message": "Logged in successfully", "success": True, "data": {"token": token.key}},
                        status=status.HTTP_200_OK)  

    
    
    
    
