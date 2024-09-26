from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate




class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'is_active', 'is_staff', 'is_superuser')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

    def create(self, validated_data):
        # Extract password and remove 'password2' from validated_data
        password = validated_data.pop('password2')
        
        # Create user instance
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Both username and password are required')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Invalid username or password')

        # Assuming `token` method is used to get JWT tokens
        token = user.token()  # Ensure this method returns a valid token

        print("toooookan",token)

        # Return token and user info in validated data
        return {
            'token': token,
            'username': user.username,
            'email': user.email,
            'id': user.id
        }