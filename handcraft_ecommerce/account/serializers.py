from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone', 'usertype', 'address', 'shopname', 'ssn')

class SignUpSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'profile')
        extra_kwargs = {
            'password': {'required': True, 'allow_blank': False, 'min_length': 8},
            'email': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'username': {},
        }

    def validate_profile(self, value):
        """
        Validate the profile data, including the 'ssn' field.
        """
        ssn = value.get('ssn')
        password = value.get('password')
    
        if len(str(ssn)) != 14:
            raise serializers.ValidationError("SSN must be 14 characters long.")
    
        if password and len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
    
        return value
    
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')  # Pop password for later use
        user = User.objects.create(**validated_data)  # Create user instance

        # Create profile instance and associate it with the user
        Profile.objects.create(user=user, **profile_data)

        user.set_password(password)  # Set password
        user.save()  # Save user instance

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
