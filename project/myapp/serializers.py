# serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        
    def create(self, validated_data):
        user_exist = User.objects.filter(email=validated_data.get("email")).exists()
        if user_exist:
            password = validated_data.pop("password")
            instance = self.Meta.model(**validated_data)
            email = validated_data.get("email")
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance
        else:
            return serializers.ValidationError("User already exists")