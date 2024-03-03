from rest_framework import serializers
from .models import User
import re
from .app import upload_photo
import os
from django.core.files.uploadedfile import TemporaryUploadedFile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'phone', 'usertype', 'address', 'shopname', 'ssn', 'is_superuser','is_active']
        # not show pass to user
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False, 'min_length': 3, 'max_length': 10},
            'last_name': {'required': True, 'allow_blank': False, 'min_length': 3, 'max_length': 10},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8, 'write_only': True},
            # 'username': {},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        # script_dir = os.path.dirname(os.path.abspath(__file__))
        # upload_photo(os.path.join(script_dir, "4.jpg"),5)
        # upload_photo(validated_data['image'],88)
        # print(validated_data['image'])
        # if isinstance(validated_data['image'], TemporaryUploadedFile):
        #     image_path = validated_data['image'].temporary_file_path()
        # else:
        #     # Assuming 'image' contains the file path
        #     image_path = validated_data['image']

        # Call the upload_photo function after saving the instance
        # upload_photo(image_path, 99)


        instance.save()
        return instance
    
    # update furst name , last , phone , address , 
    def update(self, instance, validated_data):
        instance.first_name=validated_data['first_name']
        instance.last_name=validated_data['last_name']
        # instance.email=validated_data['email']
        # password = validated_data.get('password')
        # if password is not None:
        #     instance.set_password(password)
        instance.phone=validated_data['phone']
        # instance.ssn=validated_data['ssn']
        instance.address=validated_data['address']
        
        instance.save()
        return instance
    
    # first_name must 3 to 10 characters
    def validate_first_name(self, value):
        if not (3 <= len(value) <= 10):
            raise serializers.ValidationError("First name must be between 3 and 10 characters.")
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only alphabetic characters.")
        return value
    
    # last_name must 3 to 10 characters
    def validate_last_name(self, value):
        if not (3 <= len(value) <= 10):
            raise serializers.ValidationError("Last name must be between 3 and 10 characters.")
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only alphabetic characters.")
        return value
    
    # ssn must be unique and 14 digit
    # def validate_ssn(self, value):
    #     if not value.isdigit() or len(value) != 14:
    #         raise serializers.ValidationError("SSN must be 14 digits.")
    #     if User.objects.filter(ssn=value).exists():
    #         raise serializers.ValidationError("SSN must be unique.")
    #     return value
    
    # phone must 11 digit
    # def validate_phone(self, value):
    #     if not re.match(r'^01\d{9}$', value):
    #         raise serializers.ValidationError("Phone not valid.")
    #     return value
        
    def validate_password(self, value):
        pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')
        if not pattern.match(value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter, one lowercase letter, and be at least 8 characters long."
            )
        return value
    
    # vendor must enter ssn and shopname
    def validate(self, data):
        usertype = data.get('usertype')
        ssn = data.get('ssn')
        shopname = data.get('shopname')

        if usertype == 'vendor':
            if User.objects.filter(ssn=ssn).exists():
                raise serializers.ValidationError("SSN must be unique.")
            if not ssn:
                raise serializers.ValidationError("SSN is required for vendor.")
            if not shopname:
                raise serializers.ValidationError("Shopname is required for vendor.")
        
        return data
