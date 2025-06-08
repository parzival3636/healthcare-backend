from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Patient, Doctor, PatientDoctorMapping

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must provide username and password')
        return attrs

class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class DoctorSerializer(serializers.ModelSerializer):
    patient_count = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_patient_count(self, obj):
        return obj.patient_mappings.filter(is_active=True).count()

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = '__all__'
        read_only_fields = ['assigned_date']

    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor, is_active=True).exists():
            raise serializers.ValidationError("This doctor is already assigned to this patient")
        request_user = self.context['request'].user
        if patient.created_by != request_user:
            raise serializers.ValidationError("You can only assign doctors to your own patients")
        return attrs

class PatientDoctorListSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'doctor', 'assigned_date', 'notes', 'is_active']
