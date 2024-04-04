# serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        
    def create(self, validated_data):
        try :
            email = validated_data.get("email")
            user = User.objects.get(email=email)
            if user.exists():
                return serializers.ValidationError("User already exists")
        except User.DoesNotExist:
            password = validated_data.pop("password")
            instance = self.Meta.model(**validated_data)
            email = validated_data.get("email")
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance