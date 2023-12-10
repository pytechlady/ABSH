from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}, min_length=8
    )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        if not attrs.get("username") or not attrs.get("password"):
            raise serializers.ValidationError("Fields cannot be empty")
        return attrs

    class Meta:
        model = User
        fields = ("id", "username", "password", "phone", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "phone",
            "gender",
            "age",
            "blood_group",
            "genotype",
            "occupation",
            "marital_status",
            "allergies",
            "created_at",
            "updated_at",
        )


class AuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "created_at", "updated_at")
        # read_only_fields = ('id', 'created_at', 'updated_at')


class DoctorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}, min_length=8
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
        )
        # read_only_fields = ('id', 'created_at', 'updated_at')


class DocAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "created_at", "updated_at")


class DocSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}, min_length=8
    )

    def create(self, validated_data):
        # Extract password from validated_data
        password = validated_data.pop("password", None)

        # Create the User instance
        user = User.objects.create_doctor(**validated_data)

        # Set the password for the user
        user.set_password(password)
        user.save()

        return user

    def validate(self, attrs):
        if not attrs.get("username") or not attrs.get("password"):
            raise serializers.ValidationError("Fields cannot be empty")
        return attrs

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
