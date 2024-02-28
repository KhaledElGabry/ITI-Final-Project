from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Profile
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'phone', 'usertype', 'address', 'shopname', 'ssn', 'is_superuser']
        # not show pass to user
        extra_kwargs = {
            'password': {'required': True, 'allow_blank': False, 'min_length': 8, 'write_only': True},
            'email': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            # 'username': {},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate_ssn(self, value):
        if not value.isdigit() or len(value) != 14:
            raise serializers.ValidationError("SSN must be 14 digits.")
        return value
    
    #  vendor ==> ssn shopname (required)
    # phone must digit
    # if user_instance.profile.usertype == 'vendor' and (not profile_data.get('shopname') or not profile_data.get('ssn')):
    #             return Response({'error': 'Shop name and ssn are required for vendors.'}, status=status.HTTP_400_BAD_REQUEST)

    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
    # def validate_usertype(self, value):
    #     # Only apply this validation for non-admin users
    #     if not self.instance.is_superuser:
    #         if not value:
    #             raise serializers.ValidationError('User type is required for users.')
    #     return value
    
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ('phone', 'usertype', 'address', 'shopname', 'ssn')

# class SignUpSerializer(serializers.ModelSerializer):
#     profile = UserProfileSerializer()

#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'username', 'email', 'password', 'profile')
#         extra_kwargs = {
#             'password': {'required': True, 'allow_blank': False, 'min_length': 8},
#             'email': {'required': True, 'allow_blank': False},
#             'first_name': {'required': True, 'allow_blank': False},
#             'last_name': {'required': True, 'allow_blank': False},
#             'username': {},
#         }

#     def validate_profile(self, value):
#         """
#         Validate the profile data, including the 'ssn' field.
#         """
#         ssn = value.get('ssn')
#         password = value.get('password')
    
#         if len(str(ssn)) != 14:
#             raise serializers.ValidationError("SSN must be 14 characters long.")
    
#         if password and len(password) < 8:
#             raise serializers.ValidationError("Password must be at least 8 characters long.")
    
#         return value
    
    
#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile')
#         password = validated_data.pop('password')  # Pop password for later use
#         user = User.objects.create(**validated_data)  # Create user instance

#         # Create profile instance and associate it with the user
#         Profile.objects.create(user=user, **profile_data)

#         user.set_password(password)  # Set password
#         user.save()  # Save user instance

#         return user

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'username', 'email', 'password')
