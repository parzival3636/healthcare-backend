# File: api/views.py
from rest_framework import generics, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    PatientSerializer, DoctorSerializer,
    PatientDoctorMappingSerializer, PatientDoctorListSerializer
)
from .permissions import IsOwnerOrReadOnly, IsPatientOwner

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Doctor.objects.all()
        specialization = self.request.query_params.get('specialization')
        available = self.request.query_params.get('available')
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        if available:
            queryset = queryset.filter(is_available=available.lower() == 'true')
        return queryset

class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOwner]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__created_by=self.request.user,
            is_active=True
        )

    def retrieve(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
        mappings = PatientDoctorMapping.objects.filter(
            patient=patient,
            is_active=True
        )
        serializer = PatientDoctorListSerializer(mappings, many=True)
        return Response({
            'patient': PatientSerializer(patient).data,
            'assigned_doctors': serializer.data
        })

    def destroy(self, request, pk=None):
        mapping = get_object_or_404(
            PatientDoctorMapping,
            pk=pk,
            patient__created_by=request.user
        )
        mapping.is_active = False
        mapping.save()
        return Response({
            'message': 'Doctor successfully removed from patient'
        }, status=status.HTTP_200_OK)
